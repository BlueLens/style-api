
import os
import time
from bluelens_log import Logging
from swagger_server.models.get_feed_response import GetFeedResponse
from .feed import Feed

REDIS_SERVER = os.environ['REDIS_SEARCH_SERVER']
REDIS_PASSWORD = os.environ['REDIS_SEARCH_PASSWORD']

options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='style-api:Feeds')

class Feeds(object):
  def __init__(self):
    super().__init__()

  @staticmethod
  def get_feeds(offset=None, limit=None):
    feed = Feed(log)
    res = GetFeedResponse()
    start_time = time.time()

    try:
      feeds = feed.feeds(offset, limit)
      res.message = 'Successful'
      res.data = feeds

      response_status = 200
    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('get_feeds time: ' + str(elapsed_time))
    return res, response_status


