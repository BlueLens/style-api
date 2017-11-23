
import os
from bluelens_log import Logging
from swagger_server.models.get_feed_response import GetFeedResponse
from .feed import Feed

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='style-api:Products')

class Feeds(object):
  def __init__(self):
    super().__init__()

  @staticmethod
  def get_feeds():
    feed = Feed(log)
    res = GetFeedResponse()

    try:
      feeds = feed.feeds()
      res.message = 'Successful'
      res.data = feeds

      response_status = 200
    except Exception as e:
      log.error(str(e))
      response_status = 400

    return res, response_status


