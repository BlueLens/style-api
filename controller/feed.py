import os
import redis
import pickle
from random import randint
from swagger_server.models.image import Image

REDIS_SERVER = os.environ['REDIS_SEARCH_SERVER']
REDIS_PASSWORD = os.environ['REDIS_SEARCH_PASSWORD']

REDIS_SEARCH_OBJECT_SERVER_0 = os.environ['REDIS_SEARCH_OBJECT_SERVER_0']
REDIS_SEARCH_OBJECT_PASSWORD_0 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_0']
REDIS_SEARCH_OBJECT_SERVER_1 = os.environ['REDIS_SEARCH_OBJECT_SERVER_1']
REDIS_SEARCH_OBJECT_PASSWORD_1 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_1']
REDIS_SEARCH_OBJECT_SERVER_2 = os.environ['REDIS_SEARCH_OBJECT_SERVER_2']
REDIS_SEARCH_OBJECT_PASSWORD_2 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_2']
REDIS_SEARCH_OBJECT_SERVER_3 = os.environ['REDIS_SEARCH_OBJECT_SERVER_3']
REDIS_SEARCH_OBJECT_PASSWORD_3 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_3']
REDIS_SEARCH_OBJECT_SERVER_4 = os.environ['REDIS_SEARCH_OBJECT_SERVER_4']
REDIS_SEARCH_OBJECT_PASSWORD_4 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_4']
REDIS_SEARCH_OBJECT_SERVER_5 = os.environ['REDIS_SEARCH_OBJECT_SERVER_5']
REDIS_SEARCH_OBJECT_PASSWORD_5 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_5']
REDIS_SEARCH_OBJECT_SERVER_6 = os.environ['REDIS_SEARCH_OBJECT_SERVER_6']
REDIS_SEARCH_OBJECT_PASSWORD_6 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_6']

REDIS_SEARCH_IMAGE_SERVER_0   = os.environ['REDIS_SEARCH_IMAGE_SERVER_0']
REDIS_SEARCH_IMAGE_PASSWORD_0 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_0']
REDIS_SEARCH_IMAGE_SERVER_1   = os.environ['REDIS_SEARCH_IMAGE_SERVER_1']
REDIS_SEARCH_IMAGE_PASSWORD_1 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_1']
REDIS_SEARCH_IMAGE_SERVER_2   = os.environ['REDIS_SEARCH_IMAGE_SERVER_2']
REDIS_SEARCH_IMAGE_PASSWORD_2 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_2']
REDIS_SEARCH_IMAGE_SERVER_3   = os.environ['REDIS_SEARCH_IMAGE_SERVER_3']
REDIS_SEARCH_IMAGE_PASSWORD_3 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_3']
REDIS_SEARCH_IMAGE_SERVER_4   = os.environ['REDIS_SEARCH_IMAGE_SERVER_4']
REDIS_SEARCH_IMAGE_PASSWORD_4 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_4']
REDIS_SEARCH_IMAGE_SERVER_5   = os.environ['REDIS_SEARCH_IMAGE_SERVER_5']
REDIS_SEARCH_IMAGE_PASSWORD_5 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_5']

REDIS_INDEXED_IMAGE_HASH = 'bl_indexed_image_hash'
REDIS_INDEXED_IMAGE_LIST = 'bl:indexed:image:list'
REDIS_INDEXED_OBJECT_LIST = 'bl:indexed:object:list'
REDIS_INDEXED_OBJECT_HASH = 'bl_indexed_object_hash'

CACHE_MAX_NUM = 7000

rconn = redis.StrictRedis(REDIS_SERVER, decode_responses=False, port=6379, password=REDIS_PASSWORD)

rconn_search_object_0 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_0, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_0)
rconn_search_object_1 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_1, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_1)
rconn_search_object_2 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_2, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_2)
rconn_search_object_3 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_3, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_3)
rconn_search_object_4 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_4, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_4)
rconn_search_object_5 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_5, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_5)
rconn_search_object_6 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_6, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_6)

rconn_search_image_0 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_0, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_0)
rconn_search_image_1 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_1, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_1)
rconn_search_image_2 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_2, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_2)
rconn_search_image_3 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_3, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_3)
rconn_search_image_4 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_4, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_4)
rconn_search_image_5 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_5, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_5)

class Feed:
  def __init__(self, log):
    log.info('init')
    self.log = log

  def feeds(self, offset=None, limit=None):

    feeds = []
    image_ids = []
    size = rconn.llen(REDIS_INDEXED_IMAGE_LIST)
    if size > CACHE_MAX_NUM:
      size = CACHE_MAX_NUM

    x = [randint(1, size) for p in range(1, size)]
    for i in x:
      image_id = rconn.lindex(REDIS_INDEXED_IMAGE_LIST, i)
      image_ids.append(image_id.decode('utf-8'))

    images_d = rconn_search_image_0.hmget(REDIS_INDEXED_IMAGE_HASH, image_ids)
    for image_d in images_d:
      img = Image()
      image = pickle.loads(image_d)
      image['id'] = str(image['_id'])
      i = img.from_dict(image)
      feeds.append(i)
    return feeds
