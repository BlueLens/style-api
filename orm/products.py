
import os
import time
from bluelens_log import Logging
from swagger_server.models.get_products_response import GetProductsResponse
from .search import Search

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='style-api:Products')

class Products(object):
  def __init__(self):
    super().__init__()

  @staticmethod
  def get_products(file):
    search = Search(log)
    res = GetProductsResponse()
    start_time = time.time()

    try:
      products = search.search_image(file)

      res.message = 'Successful'
      res.data = products

      response_status = 200
    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('get_products time: ' + str(elapsed_time))
    return res, response_status


