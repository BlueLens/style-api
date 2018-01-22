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

REDIS_INDEXED_SIM_IMAGES_HASH = 'bl_indexed_image_hash'
REDIS_INDEXED_IMAGE_HASH = 'bl_indexed_image_hash'
REDIS_INDEXED_IMAGE_HASH_MAP = 'bl_indexed_image_hash_map'
REDIS_INDEXED_IMAGE_LIST = 'bl:indexed:image:list'
REDIS_INDEXED_OBJECT_HASH = 'bl_indexed_object_hash'
REDIS_INDEXED_OBJECT_HASH_MAP = 'bl_indexed_object_hash_map'
REDIS_INDEXED_OBJECT_LIST = 'bl:indexed:object:list'

REDIS_USER_OBJECT_HASH = 'bl:user:object:hash'
REDIS_USER_IMAGE_HASH = 'bl:user:image:hash'

REDIS_LOG_SEARCH_IMAGE_FILE_QUEUE = 'bl:log:search:image:file'
REDIS_LOG_SEARCH_IMAGE_ID_QUEUE = 'bl:log:search:image:id'
REDIS_LOG_SEARCH_OBJECT_ID_QUEUE = 'bl:log:search:object:id'

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
  def get_images(image_id, offset=0, limit=10):
    log.info('get_images:' + image_id)
    index_image_api = IndexImages()
    res = GetImageResponse()

    try:
      image_d = rconn.hget(REDIS_INDEXED_SIM_IMAGES_HASH, image_id)

      if image_d != None:
        images_dic = pickle.loads(image_d)
      else:
        images_dic = index_image_api.get_sim_images(image_id)

      images = []
      for image in images_dic:
        img = Image()
        image = img.from_dict(image)
        images.append(image)

      rconn.hset(REDIS_INDEXED_SIM_IMAGES_HASH, image_id, pickle.dumps(images_dic))

      res.data = images
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
    user_api = Users()
    res = GetImageResponse()

    log_dic = {}
    log_dic['device_id'] = 'bluehackmaster'
    log_dic['object_id'] = object_id
    rconn.lpush(REDIS_LOG_SEARCH_OBJECT_ID_QUEUE, pickle.dumps(log_dic))
    try:
      object_d = rconn.hget(REDIS_USER_OBJECT_HASH, object_id)

      if object_d != None:
        images = pickle.loads(object_d)
      else:
        object= user_api.get_object(object_id)
        images = search.get_images_by_object_vector(object['feature'], limit=limit)

      images_list = []
      if images is None:
        res.message = "Successful, but there is no similar images"
        res.data = None
        response_status = 400
      else:
        for image in images:
          images_list.append(Image().from_dict(image))

        res.message = "Successful"
        res.data = images_list
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
