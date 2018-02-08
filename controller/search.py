import time

from PIL import Image
import numpy as np
import io
import os
import uuid
import redis
import pickle
import urllib.request
from stylelens_feature import feature_extract
from stylelens_search_vector.vector_search import VectorSearch
from stylelens_detect.object_detect import ObjectDetector

from swagger_server.models.boxes_array import BoxesArray
from swagger_server.models.box_object import BoxObject
from swagger_server.models.box import Box
from stylelens_object.objects import Objects
from stylelens_image.images import Images
from stylelens_index.index_images import IndexImages
from stylelens_index.index_objects import IndexObjects
from stylelens_product.products import Products

VECTOR_SIMILARITY_THRESHHOLD = 250
DETECT_IMAGE_RESIZE_WIDTH = 380
DETECT_IMAGE_RESIZE_HEIGHT= 380

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

REDIS_SERVER = os.environ['REDIS_SEARCH_SERVER']
REDIS_PASSWORD = os.environ['REDIS_SEARCH_PASSWORD']

OD_HOST = os.environ['OD_HOST']
OD_PORT = os.environ['OD_PORT']

DB_OBJECT_HOST = os.environ['DB_OBJECT_HOST']
DB_OBJECT_PORT = os.environ['DB_OBJECT_PORT']
DB_OBJECT_NAME = os.environ['DB_OBJECT_NAME']
DB_OBJECT_USER = os.environ['DB_OBJECT_USER']
DB_OBJECT_PASSWORD = os.environ['DB_OBJECT_PASSWORD']

SEARCH_HOST = os.environ['VECTOR_SEARCH_HOST']
SEARCH_PORT = os.environ['VECTOR_SEARCH_PORT']

REDIS_INDEXED_IMAGE_HASH = 'bl_indexed_image_hash'
REDIS_INDEXED_IMAGE_LIST = 'bl:indexed:image:list'
REDIS_INDEXED_OBJECT_HASH = 'bl_indexed_object_hash'
REDIS_INDEXED_OBJECT_LIST = 'bl:indexed:object:list'

REDIS_KEY_OBJECT_LIST = 'bl:object:list'
REDIS_OBJECT_HASH = 'bl:object:hash'
REDIS_PRODUCT_HASH = 'bl:product:hash'
REDIS_PRODUCTS_BY_PRODUCT_HASH = 'bl:products:by:product'
TMP_CROP_IMG_FILE = 'tmp.jpg'

rconn = redis.StrictRedis(REDIS_SERVER, port=6379, password=REDIS_PASSWORD)

class Search:
  def __init__(self, log):
    log.info('init')
    self.image_feature = feature_extract.ExtractFeature(use_gpu=True)
    self.log = log
    self.vector_search = VectorSearch()
    self.object_detector = ObjectDetector()
    self.object_api = Objects()
    self.image_api = Images()
    self.index_image_api = IndexImages()

  def get_images_by_object_vector(self, vector, offset=0, limit=10):
    return self.get_images_by_vector(vector, offset=offset, limit=limit)

  def search_image_file(self, file, offset=0, limit=5):
    feature = self.extract_feature(file)
    return self.get_images_by_vector(feature, offset=offset, limit=limit)

  def search_image_data(self, image_data, offset=0, limit=10):

    start_time = time.time()
    im = Image.open(io.BytesIO(image_data))
    size = 380, 380
    im.thumbnail(size, Image.ANTIALIAS)
    # im.show()
    file_name = str(uuid.uuid4()) + '.jpg'
    im.save(file_name)
    feature = self.extract_feature(file_name)
    print(feature.dtype)
    elapsed_time = time.time() - start_time
    self.log.info('search_image time: ' + str(elapsed_time))
    return self.get_images_by_vector(feature, offset, limit)

  def get_images_by_vector(self, vector, offset=0, limit=5):
    try:
      # Query to search vector
      start_time = time.time()

      vector_d, vector_i = self.vector_search.search(vector, limit)
      distances = np.fromstring(vector_d, dtype=np.float32)
      ids = np.fromstring(vector_i, dtype=np.int)

      elapsed_time = time.time() - start_time
      self.log.debug('vector search time: ' + str(elapsed_time))
      # pprint(api_response)
    except Exception as e:
      self.log.error("Exception when calling SearchApi->search_vector: %s\n" % e)


    arr_i = []
    i = 0
    for d in distances:
      print(d)
      if d <= VECTOR_SIMILARITY_THRESHHOLD:
        if i < limit:
          arr_i.append(ids[i])
        else:
          break
        i = i+ 1

    if len(arr_i) > 0:
      ids = [int(x) for x in arr_i]

      try:
        start_time = time.time()
        objects = self.object_api.get_objects_by_indexes(ids)
        elapsed_time = time.time() - start_time
        print(elapsed_time)
        images = self.get_images_from_objects(objects)
        return images
      except Exception as e:
        self.log.error('Trying Objects.get_objects_by_indexes():' + str(e))
        return None

    # obj_ids = self.get_object_ids(arr_i)
    # prod_ids = self.get_image_ids(obj_ids)

    # if len(arr_i) > 5:
    #   # Using MongoDB
    #   products_info = self.get_products_from_db(prod_ids, offset=offset, limit=limit)
    # else:
    #   # Using Redis
    #   products_info = self.get_image_info(prod_ids, offset=offset, limit=limit)
    return None

  def get_images_from_objects(self, objects):
    limit = 10
    image_ids = []

    for obj in objects:
      image_ids.append(obj['image_id'])

    ids = list(set(image_ids))
    try:
      start_time = time.time()
      _images = self.image_api.get_images_by_ids(ids)
      elapsed_time = time.time() - start_time
      print(elapsed_time)
      images = []
      for image in _images:
        image['id'] = str(image.pop('_id'))
        image.pop('images', None)
        images.append(image)
      return images
    except Exception as e:
      self.log.error(str(e))
      return None

    return images

  def get_products_from_db(self, ids, offset=0, limit=5):
    self.log.debug('get_products_from_db')
    start_time = time.time()
    product_api = None
    # product_api = stylelens_product.ProductApi()
    try:
      api_response = product_api.get_products_by_ids(ids)
    except Exception as e:
      self.log.error("Exception when calling ProductApi->get_products_by_ids: %s\n" % e)
    elapsed_time = time.time() - start_time
    self.log.debug('get_products_from_db time: ' + str(elapsed_time))

    products_info = []

    for id in ids:
      i = id.decode('utf-8')
      for p in api_response.data:
        if i == p.id:
          products_info.append(p.to_dict())
          break

    return products_info

  def get_object_ids(self, ids):
    obj_ids = []
    for i in ids:
      id = rconn.lindex(REDIS_INDEXED_OBJECT_LIST, i - 1)
      obj_ids.append(id.decode('utf-8'))
    self.log.debug(obj_ids)
    return obj_ids

  def get_image_ids(self, ids):
    self.log.debug('get_product_ids' + str(ids))
    product_ids = rconn.hmget(REDIS_INDEXED_IMAGE_HASH, ids)
    # self.log.debug(product_ids)
    return product_ids

  def get_image_info(self, ids, offset=0, limit=5):
    self.log.debug('get_product_info' + str(ids))
    products = []
    products_info = rconn.hmget(REDIS_PRODUCT_HASH, ids)
    i = 0
    for p in products_info:
      if i < limit:
        product = pickle.loads(p)
        product['sub_images'] = None
        product['sub_images_mobile'] = None
        products.append(product)
      i = i + 1
    return products

  def allowed_file(self, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

  def extract_feature(self, file):
    feature_vector = self.image_feature.extract_feature(file)
    # feature = np.fromstring(feature_vector, dtype=np.float32)
    return feature_vector

  def get_product_info(self, index):
    start_time = time.time()
    obj_id = rconn.lindex(REDIS_KEY_OBJECT_LIST, index-1)
    obj_id = obj_id.decode('utf-8')
    # self.log.debug(obj_id)

    product_id = rconn.hget(REDIS_OBJECT_HASH, obj_id)
    # self.log.debug(product_id)
    product_id = product_id.decode('utf-8')
    # self.log.debug(product_id)

    product = rconn.hget(REDIS_PRODUCT_HASH, product_id)
    # self.log.debug(product)
    product = pickle.loads(product)
    # self.log.debug('get_product_info: done')
    elapsed_time = time.time() - start_time
    # self.log.info('get_product_info time: ' + str(elapsed_time))
    return product

  def get_objects(self, image_file, products_offset=0, products_limit=5):
    start_time = time.time()

    objects = self.object_detector.getObjects(file=image_file)

    boxes_array = []
    objects_array = []
    feature = []
    best_score = -1
    best_score_index = 0
    i = 0
    for object in objects:
      obj = {}
      box_object = BoxObject()
      box_object.class_name = object.class_name
      obj['class_name'] = object.class_name
      box_object.class_code = object.class_code
      obj['class_code'] = object.class_code
      box_object.score = object.score
      obj['score'] = object.score

      if best_score_index < object.score:
        best_score_index = object.score
        best_score = object.score
        best_score_index = i
        # arr = np.fromstring(object.feature, dtype=np.float32)
        # feature = arr
      # self.log.debug(object.class_name)
      # self.log.debug(object.class_code)
      # self.log.debug(object.location)
      box = Box()
      box_dic = {}
      box.left = object.location.left
      box_dic['left'] = object.location.left
      box.right = object.location.right
      box_dic['right'] = object.location.right
      box.top = object.location.top
      box_dic['top'] = object.location.top
      box.bottom = object.location.bottom
      box_dic['bottom'] = object.location.bottom
      box_object.box = box
      obj['box'] = box_dic

      obj['feature'] = object.feature
      # self.log.debug(box)
      boxes_array.append(box_object)
      objects_array.append(obj)
      i = i + 1

    if best_score == -1:
      box_object = BoxObject()
      box_object.class_name = 'na'
      box_object.class_code = 'na'
      box_object.score = '-1'

      box = Box()
      box.left = -1
      box.right = -1
      box.top = -1
      box.bottom = -1
      box_object.box = box
      boxes_array.append(box_object)
      # products = self.search_image_data(image_data, offset=products_offset, limit=products_limit)
    # else:
    #   images = self.get_images_by_vector(object.feature, offset=products_offset, limit=products_limit)

    local_start_time = time.time()
    elapsed_time = time.time() - local_start_time
    self.log.info('query_feature time: ' + str(elapsed_time))
    # boxes_array[best_score_index].images = images

    elapsed_time = time.time() - start_time
    self.log.info('get_objects time: ' + str(elapsed_time))
    return boxes_array, objects_array

  def get_indexed_image(self, image_id):
    try:
      image = self.index_image_api.get_image(image_id)
    except Exception as e:
      self.log.error(str(e))
      return None

    return image

  def get_products_by_product_id(self, product_id, offset=0, limit=5):
    if rconn.hexists(REDIS_PRODUCTS_BY_PRODUCT_HASH, product_id):
      products = rconn.hget(REDIS_PRODUCTS_BY_PRODUCT_HASH, product_id)
      products = pickle.loads(products)
      return products[offset:limit]
    else:
      product = rconn.hget(REDIS_PRODUCT_HASH, product_id)
      product = pickle.loads(product)
      try:
        f = urllib.request.urlopen(product['main_image_mobile_full'])
      except Exception as e:
        self.log.error(str(e))
      boxes = self.get_objects(f, limit)

      for box in boxes:
        if box.products:
          rconn.hset(REDIS_PRODUCTS_BY_PRODUCT_HASH, product_id, pickle.dumps(box.products))
          return box.products
    return {}

  def get_products_by_keyword(self, keyword, offset=0, limit=100):
    self.log.debug('get_products_by_keyword')
    product_api = Products()
    try:
      total_count = product_api.get_products_count_by_keyword(keyword)
    except Exception as e:
      self.log.error("Exception when calling get_products_count_by_keyword: %s\n" % e)

    try:
      products = product_api.get_products_by_keyword(keyword, only_text=False, offset=offset, limit=limit)
    except Exception as e:
      self.log.error("Exception when calling get_products_by_keyword: %s\n" % e)

    return total_count, products

