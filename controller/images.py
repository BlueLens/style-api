import os
import time
import redis
import pickle
from bluelens_log import Logging
from swagger_server.models.get_images_response import GetImagesResponse
from swagger_server.models.get_image_response import GetImageResponse
from swagger_server.models.image import Image
from stylelens_index.index_images import IndexImages
from stylelens_index.index_objects import IndexObjects
from stylelens_user.users import Users

from .search import Search

REDIS_INDEXED_IMAGE_HASH = 'bl_indexed_image_hash'
REDIS_INDEXED_IMAGE_HASH_MAP = 'bl_indexed_image_hash_map'
REDIS_INDEXED_IMAGE_LIST = 'bl:indexed:image:list'
REDIS_INDEXED_OBJECT_HASH = 'bl_indexed_object_hash'
REDIS_INDEXED_OBJECT_HASH_MAP = 'bl_indexed_object_hash_map'
REDIS_INDEXED_OBJECT_LIST = 'bl:indexed:object:list'

REDIS_USER_OBJECT_HASH = 'bl:user:object:hash'
REDIS_USER_IMAGE_HASH = 'bl:user:image:hash'

REDIS_SERVER = os.environ['REDIS_SEARCH_SERVER']
REDIS_PASSWORD = os.environ['REDIS_SEARCH_PASSWORD']


CACHE_MAX_NUM = 7000

rconn = redis.StrictRedis(REDIS_SERVER, decode_responses=False, port=6379, password=REDIS_PASSWORD)

options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='style-api:Products')

class Images(object):
  def __init__(self):
    super().__init__()

  @staticmethod
  def get_images(image_id, offset, limit):
    log.info('get_images_by_id')
    start_time = time.time()
    index_image_api = IndexImages()
    res = GetImageResponse()

    try:
      image_d = rconn.hget(REDIS_INDEXED_IMAGE_HASH, image_id)

      if image_d != None:
        image_dic = pickle.loads(image_d)
      else:
        image_dic = index_image_api.get_image(image_id)

      image_dic['id'] = str(image_dic['_id'])
      image_dic.pop('_id')
      img = Image()
      image = img.from_dict(image_dic)

      res.data = image.images
      res.message = 'Successful'
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    return res, response_status

  @staticmethod
  def get_images_by_object_id(object_id, offset=0, limit=10):
    log.info('get_images_by_object_id')
    search = Search(log)
    start_time = time.time()
    user_api = Users()
    res = GetImageResponse()

    try:
      object_d = rconn.hget(REDIS_USER_OBJECT_HASH, object_id)

      if object_d != None:
        object= pickle.loads(object_d)
      else:
        object= user_api.get_object(object_id)

      images_list = []
      images = search.get_images_by_object_vector(object['feature'])
      for image in images:
        images_list.append(Image().from_dict(image))

      res.data = images_list
      res.message = 'Successful'
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    return res, response_status

  @staticmethod
  def get_images_by_user_image_file(file, offset=0, limit=5):
    search = Search(log)
    res = GetImagesResponse()
    start_time = time.time()

    try:
      images = search.search_user_image_file(file, offset, limit)

      res.message = 'Successful'
      res.data = images

      response_status = 200
    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('get_images_by_user_image_file time: ' + str(elapsed_time))
    return res, response_status

  @staticmethod
  def get_images_by_user_image_id_and_object_index(user_image_id, object_index):
    log.info('get_images_by_user_image_id_and_object_index')
    start_time = time.time()
    index_image_api = IndexImages()
    res = GetImagesResponse()
    log.debug(user_image_id)
    log.debug(object_index)

    try:
      api_res = index_image_api.get_images_by_user_image_id_and_object_index(user_image_id, object_index)
      res.message = 'Successful'
      images = []
      for p in api_res.data:
        images.append(p.to_dict())
      res.data = images
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('time: get_images_by_user_image_id_and_object_index' + str(elapsed_time))
    return res, response_status

  @staticmethod
  def get_image_by_host_code_and_product_no(host_code, product_no):
    log.info('get_image_by_host_code_and_product_no')
    start_time = time.time()
    index_image_api = IndexImages()
    res = GetImageResponse()
    image = Image()

    try:
      api_res = index_image_api.get_image_by_hostcode_and_product_no(host_code, product_no)
      res.data = image.from_dict(api_res.data.to_dict())
      res.message = 'Successful'
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('time: get_image_by_host_code_and_product_no' + str(elapsed_time))
    return res, response_status

  @staticmethod
  def get_image_by_id(image_id):
    log.info('get_image_by_id')
    start_time = time.time()
    index_image_api = IndexImages()
    res = GetImageResponse()

    try:


      image_d = rconn.hget(REDIS_INDEXED_IMAGE_HASH, image_id)

      if image_d != None:
        image_dic = pickle.loads(image_d)
      else:
        image_dic = index_image_api.get_image(image_id)

      image_dic['id'] = str(image_dic['_id'])
      image_dic.pop('_id')
      img = Image()
      image = img.from_dict(image_dic)

      res.data = image
      res.message = 'Successful'
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    return res, response_status
