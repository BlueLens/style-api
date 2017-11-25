
import os
import time
from bluelens_log import Logging
from swagger_server.models.get_products_response import GetProductsResponse
from swagger_server.models.get_product_response import GetProductResponse
from swagger_server.models.product import Product
from .search import Search
import stylelens_product
from stylelens_product.rest import ApiException

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
  def get_products(product_id, offset, limit):
    log.info('get_products')
    start_time = time.time()
    search = Search(log)
    res = GetProductsResponse()

    try:
      products = search.get_products_by_product_id(product_id, offset, limit)
      res.data = products
      res.message = 'Successful'
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('get_products time: ' + str(elapsed_time))
    return res, response_status

  @staticmethod
  def get_products_by_image_file(file):
    search = Search(log)
    res = GetProductsResponse()
    start_time = time.time()

    try:
      products = search.search_image_file(file)

      res.message = 'Successful'
      res.data = products

      response_status = 200
    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('get_products time: ' + str(elapsed_time))
    return res, response_status

  @staticmethod
  def get_products_by_image_id_and_object_id(image_id, object_id):
    log.info('get_product_by_image_id_and_object_id')
    start_time = time.time()
    product_api = stylelens_product.ProductApi()
    res = GetProductsResponse()
    log.debug(image_id)
    log.debug(object_id)

    try:
      api_res = product_api.get_products_by_image_id_and_object_id(image_id, object_id)
      res.message = 'Successful'
      products = []
      for p in api_res.data:
        products.append(p.to_dict())
      res.data = products
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('get_products_by_image_id_and_object_id time: ' + str(elapsed_time))
    return res, response_status

  @staticmethod
  def get_product_by_host_code_and_product_no(host_code, product_no):
    log.info('get_product_by_host_code_and_product_no')
    start_time = time.time()
    product_api = stylelens_product.ProductApi()
    res = GetProductResponse()
    product = Product()

    try:
      api_res = product_api.get_products_by_hostcode_and_product_no(host_code, product_no)
      res.data = product.from_dict(api_res.data.to_dict())
      res.message = 'Successful'
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('get_product_by_host_code_and_product_no time: ' + str(elapsed_time))
    return res, response_status

  @staticmethod
  def get_product_by_id(product_id):
    log.info('get_product_by_id')
    start_time = time.time()
    product_api = stylelens_product.ProductApi()
    res = GetProductResponse()
    product = Product()

    try:
      api_res = product_api.get_product_by_id(product_id)
      res.data = product.from_dict(api_res.data.to_dict())
      res.message = 'Successful'
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    return res, response_status
