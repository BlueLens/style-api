import os
import redis
import pickle
from random import randint
from swagger_server.models.image import Image
from stylelens_index.index_images import IndexImages
from stylelens_index.index_objects import IndexObjects

REDIS_SERVER = os.environ['REDIS_SEARCH_SERVER']
REDIS_PASSWORD = os.environ['REDIS_SEARCH_PASSWORD']

REDIS_INDEXED_IMAGE_HASH = 'bl_indexed_image_hash'
REDIS_INDEXED_IMAGE_LIST = 'bl:indexed:image:list'
REDIS_INDEXED_OBJECT_LIST = 'bl:indexed:object:list'
REDIS_INDEXED_OBJECT_HASH = 'bl_indexed_object_hash'

rconn = redis.StrictRedis(REDIS_SERVER, decode_responses=False, port=6379, password=REDIS_PASSWORD)

class User:
  def __init__(self, log):
    log.info('init')
    self.log = log

  def feeds(self, offset=0, limit=10):

    feeds = []
    image_ids = []

    # x = [randint(1, size) for p in range(1, size)]
    # for i in x:
    #   image_id = rconn.lindex(REDIS_INDEXED_IMAGE_LIST, i)
    #   image_ids.append(image_id.decode('utf-8'))

    # images_d = rconn_search_image_0.hmget(REDIS_INDEXED_IMAGE_HASH, image_ids)
    # for image_d in images_d:
    #   img = Image()
    #   image = pickle.loads(image_d)
    #   image['id'] = str(image['_id'])
    #   i = img.from_dict(image)
    #   feeds.append(i)
    img = Image()
    feeds.append(img)
    return feeds
