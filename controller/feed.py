import os
import redis
import pickle
from swagger_server.models.image import Image

REDIS_SERVER = os.environ['REDIS_SEARCH_SERVER']
REDIS_PASSWORD = os.environ['REDIS_SEARCH_PASSWORD']

REDIS_INDEXED_IMAGE_HASH = 'bl_indexed_image_hash'
REDIS_INDEXED_IMAGE_LIST = 'bl:indexed:image:list'
REDIS_INDEXED_OBJECT_LIST = 'bl:indexed:object:list'

rconn = redis.StrictRedis(REDIS_SERVER, decode_responses=False, port=6379, password=REDIS_PASSWORD)

class Feed:
  def __init__(self, log):
    log.info('init')
    self.log = log

  def feeds(self, offset=None, limit=None):

    feeds = []
    image_ids = []
    for i in range(offset, offset+limit):
      image_id = rconn.lindex(REDIS_INDEXED_IMAGE_LIST, i)
      image_ids.append(image_id.decode('utf-8'))

    images_d = rconn.hmget(REDIS_INDEXED_IMAGE_HASH, image_ids)
    for image_d in images_d:
      img = Image()
      image = pickle.loads(image_d)
      image['id'] = str(image['_id'])
      i = img.from_dict(image)
      feeds.append(i)
    return feeds
