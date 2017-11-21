import time

from PIL import Image
import os
import uuid
import redis
import pickle
from stylelens_feature import feature_extract
import stylelens_search_vector
from stylelens_search_vector.rest import ApiException
from pprint import pprint

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

REDIS_KEY_IMAGE_HASH = 'bl:image:hash'
REDIS_KEY_IMAGE_LIST = 'bl:image:list'

REDIS_KEY_OBJECT_LIST = 'bl:object:list'
REDIS_OBJECT_HASH = 'bl:object:hash'
REDIS_PRODUCT_HASH = 'bl:product:hash'

rconn = redis.StrictRedis(REDIS_SERVER, port=6379, password=REDIS_PASSWORD)

class Search:
  def __init__(self, log):
    log.info('init')
    self.image_feature = feature_extract.ExtractFeature(use_gpu=True)
    self.vector_search_client = stylelens_search_vector.SearchApi()
    self.log = log

  def search_imgage(self, image_file):
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
      return self.query_feature(feature.tolist())

  def query_feature(self, vector):
    body = stylelens_search_vector.VectorSearchRequest() # VectorSearchRequest |
    body.vector = vector

    try:
      # Query to search vector
      api_response = self.vector_search_client.search_vector(body)
      pprint(api_response)
    except ApiException as e:
      print("Exception when calling SearchApi->search_vector: %s\n" % e)

    if api_response.data.vector is not None:
      res_vector = api_response.data.vector
      pprint(res_vector)

    response_products = []
    # for idx in range(1, 3):
    for idx in res_vector:
      self.log.debug(idx)
      product_info = self.get_product_info(idx)
      product_info['sub_images'] = None
      response_products.append(product_info)

    return response_products

  def allowed_file(self, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

  def extract_feature(self, file):
    feature = self.image_feature.extract_feature(file)
    # print(feature)
    return feature

  def get_product_info(self, index):
    obj_id = rconn.lindex(REDIS_KEY_OBJECT_LIST, index-1)
    obj_id = obj_id.decode('utf-8')
    self.log.debug(obj_id)

    product_id = rconn.hget(REDIS_OBJECT_HASH, obj_id)
    product_id = product_id.decode('utf-8')

    product = rconn.hget(REDIS_PRODUCT_HASH, product_id)
    product = pickle.loads(product)
    self.log.debug(product)
    return product
