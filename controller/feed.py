import time

import os
import uuid
import redis
import pickle
from pprint import pprint

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

REDIS_KEY_IMAGE_HASH = 'bl:image:hash'
REDIS_KEY_IMAGE_LIST = 'bl:image:list'

REDIS_KEY_OBJECT_LIST = 'bl:object:list'
REDIS_OBJECT_HASH = 'bl:object:hash'
REDIS_PRODUCT_HASH = 'bl:product:hash'

rconn = redis.StrictRedis(REDIS_SERVER, port=6379, password=REDIS_PASSWORD)

class Feed:
  def __init__(self, log):
    log.info('init')
    self.log = log

  def feeds(self, offset=None, limit=None):

    feeds = []
    for i in range(offset, offset+limit):
      obj_id = rconn.lindex(REDIS_KEY_OBJECT_LIST, i)
      obj_id = obj_id.decode('utf-8')

      product_id = rconn.hget(REDIS_OBJECT_HASH, obj_id)
      product_id = product_id.decode('utf-8')

      product = rconn.hget(REDIS_PRODUCT_HASH, product_id)
      # self.log.debug(product)
      product = pickle.loads(product)
      product['sub_images'] = None
      feeds.append(product)
    return feeds
