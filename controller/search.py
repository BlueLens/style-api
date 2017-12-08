import time

from PIL import Image
import numpy as np
import io
import os
import uuid
import redis
import pickle
import urllib.request
import tensorflow as tf
from stylelens_feature import feature_extract
# import stylelens_search_vector
# from stylelens_search_vector.rest import ApiException
import stylelens_product
from stylelens_product.rest import ApiException
from pprint import pprint

from swagger_server.models.boxes_array import BoxesArray
from swagger_server.models.box_object import BoxObject
from swagger_server.models.box_array import BoxArray
from swagger_server.models.product import Product

import grpc
from controller import object_detect_pb2
from controller import object_detect_pb2_grpc
from controller import vector_search_pb2
from controller import vector_search_pb2_grpc


VECTOR_SIMILARITY_THRESHHOLD = 450
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

OD_HOST = os.environ['OD_HOST']
OD_PORT = os.environ['OD_PORT']

SEARCH_HOST = os.environ['SEARCH_HOST']
SEARCH_PORT = os.environ['SEARCH_PORT']

REDIS_KEY_IMAGE_HASH = 'bl:image:hash'
REDIS_KEY_IMAGE_LIST = 'bl:image:list'

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
    # self.vector_search_client = stylelens_search_vector.SearchApi()
    self.log = log

  def search_image_file(self, image_file, offset=0, limit=5):

    start_time = time.time()
    if image_file and self.allowed_file(image_file.filename):
      im = Image.open(image_file.stream)

      file_type = image_file.filename.rsplit('.', 1)[1]
      if 'jpg' == file_type or 'JPG' == file_type or 'jpeg' == file_type or 'JPEG' == file_type:
        print('jpg')
      else:
        bg = Image.new("RGB", im.size, (255,255,255))
        bg.paste(im, (0,0), im)
        bg.save('file.jpg', quality=95)
        im = bg
      im.show()
      size = 300, 300
      im.thumbnail(size, Image.ANTIALIAS)
      # im.show()
      file_name = str(uuid.uuid4()) + '.jpg'
      im.save(file_name)
      feature = self.extract_feature(file_name)
      print(feature.dtype)
      elapsed_time = time.time() - start_time
      self.log.info('search_image time: ' + str(elapsed_time))
      return self.query_feature(feature.tolist(), offset=offset, limit=limit)

  def search_image_data(self, image_data, offset=0, limit=10):

    start_time = time.time()
    im = Image.open(io.BytesIO(image_data))
    size = 300, 300
    im.thumbnail(size, Image.ANTIALIAS)
    # im.show()
    file_name = str(uuid.uuid4()) + '.jpg'
    im.save(file_name)
    feature = self.extract_feature(file_name)
    print(feature.dtype)
    elapsed_time = time.time() - start_time
    self.log.info('search_image time: ' + str(elapsed_time))
    return self.query_feature(feature.tolist(), offset, limit)

  def query_feature(self, vector, offset=0, limit=5):
    try:
      # Query to search vector
      start_time = time.time()
      channel = grpc.insecure_channel(SEARCH_HOST + ':' + SEARCH_PORT)
      stub = vector_search_pb2_grpc.SearchStub(channel)
      v = np.asarray(vector, dtype=np.float32)
      results = stub.SearchVector(vector_search_pb2.SearchRequest(vector=v.tobytes(),
                                                                  candidate=limit))
      # print(results)
      # d = results.vector_d
      # i = results.vector_i
      distances = np.fromstring(results.vector_d, dtype=np.float32)
      ids = np.fromstring(results.vector_i, dtype=np.int)
      elapsed_time = time.time() - start_time
      self.log.debug('vector search time: ' + str(elapsed_time))
      # pprint(api_response)
    except ApiException as e:
      self.log.error("Exception when calling SearchApi->search_vector: %s\n" % e)


    arr_i = []
    i = 0
    for d in distances:
      if d <= VECTOR_SIMILARITY_THRESHHOLD:
        if i < limit:
          arr_i.append(ids[i])
        else:
          break
        i = i+ 1

    obj_ids = self.get_object_ids(arr_i)
    prod_ids = self.get_product_ids(obj_ids)

    if len(arr_i) > 5:
      # Using MongoDB
      products_info = self.get_products_from_db(prod_ids, offset=offset, limit=limit)
    else:
      # Using Redis
      products_info = self.get_products_info(prod_ids, offset=offset, limit=limit)
    return products_info

  def get_products_from_db(self, ids, offset=0, limit=5):
    self.log.debug('get_products_from_db')
    start_time = time.time()
    product_api = stylelens_product.ProductApi()
    try:
      api_response = product_api.get_products_by_ids(ids)
    except ApiException as e:
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
      id = rconn.lindex(REDIS_KEY_OBJECT_LIST, i - 1)
      obj_ids.append(id.decode('utf-8'))
    self.log.debug(obj_ids)
    return obj_ids

  def get_product_ids(self, ids):
    self.log.debug('get_product_ids' + str(ids))
    product_ids = rconn.hmget(REDIS_OBJECT_HASH, ids)
    # self.log.debug(product_ids)
    return product_ids

  def get_products_info(self, ids, offset=0, limit=5):
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
    feature = self.image_feature.extract_feature(file)
    return feature

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

  def get_objects(self, image_data, products_offset=0, products_limit=5):
    start_time = time.time()
    channel = grpc.insecure_channel(OD_HOST + ':' + OD_PORT)
    stub = object_detect_pb2_grpc.DetectStub(channel)

    # with tf.gfile.GFile(file, 'rb') as fid:
    #   image_data = fid.read()
    local_start_time = time.time()
    objects = stub.GetObjects(object_detect_pb2.DetectRequest(file_data=image_data))
    elapsed_time = time.time() - local_start_time
    self.log.info('local_get_objects time: ' + str(elapsed_time))

    boxes_array = []
    feature = []
    best_score = -1
    best_score_index = 0
    i = 0
    for object in objects:
      box_object = BoxObject()
      box_object.class_name = object.class_name
      box_object.class_code = object.class_code
      box_object.score = object.score

      if best_score_index < object.score:
        best_score_index = object.score
        best_score = object.score
        best_score_index = i
        arr = np.fromstring(object.feature, dtype=np.float32)
        feature = arr
      # self.log.debug(object.class_name)
      # self.log.debug(object.class_code)
      # self.log.debug(object.location)
      box = []
      box.append(object.location.left)
      box.append(object.location.right)
      box.append(object.location.top)
      box.append(object.location.bottom)
      box_object.box = box
      # self.log.debug(box)
      boxes_array.append(box_object)
      i = i + 1

    if best_score == -1:
      box_object = BoxObject()
      box_object.class_name = 'na'
      box_object.class_code = 'na'
      box_object.score = '-1'
      box_object.box = [-1, -1, -1, -1]
      boxes_array.append(box_object)
      products = self.search_image_data(image_data, offset=products_offset, limit=products_limit)
    else:
      products = self.query_feature(feature.tolist(), offset=products_offset, limit=products_limit)

    local_start_time = time.time()
    elapsed_time = time.time() - local_start_time
    self.log.info('query_feature time: ' + str(elapsed_time))
    boxes_array[best_score_index].products = products

    elapsed_time = time.time() - start_time
    self.log.info('get_objects time: ' + str(elapsed_time))
    return boxes_array

  def get_objects_by_product_id(self, product_id, products_limit=5):
    product = rconn.hget(REDIS_PRODUCT_HASH, product_id)
    product = pickle.loads(product)
    try:
      f = urllib.request.urlopen(product['main_image_mobile_full'])
    except Exception as e:
      self.log.error(str(e))
    image_data = f.fp.read()
    boxes = self.get_objects(image_data, products_limit)
    return boxes

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
      image_data = f.fp.read()
      boxes = self.get_objects(image_data, limit)

      for box in boxes:
        if box.products:
          rconn.hset(REDIS_PRODUCTS_BY_PRODUCT_HASH, product_id, pickle.dumps(box.products))
          return box.products
    return {}

