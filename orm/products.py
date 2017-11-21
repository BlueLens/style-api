
import os
from bson.objectid import ObjectId
from orm.database import DataBase
from swagger_server.models.product import Product
from swagger_server.models.add_product_response import AddProductResponse
from swagger_server.models.get_product_response import GetProductResponse
from swagger_server.models.get_products_response import GetProductsResponse
from swagger_server.models.delete_product_response import DeleteProductResponse
from swagger_server.models.add_product_response_data import AddProductResponseData

from swagger_server.models.update_product_response import UpdateProductResponse

from bluelens_log import Logging

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='style-api:Products')

class Products(DataBase):
  def __init__(self):
    super().__init__()
    self.products = self.db.products

  @staticmethod
  def add_product(connexion):
    orm = Products()
    res = AddProductResponse()
    data = AddProductResponseData()
    response_status = 200
    if connexion.request.is_json:
      product = connexion.request.get_json()

      try:
        r = orm.products.insert(product)
        res.message = 'Successful'
        data.product_id = str(r)
        res.data = data
      except Exception as e:
        res.message = str(e)
        response_status = 400

    log.debug(res)
    return res, response_status

  @staticmethod
  def update_product(connexion):
    log.info('update_product')
    orm = Products()
    res = UpdateProductResponse()
    response_status = 200
    if connexion.request.is_json:
      product_json = connexion.request.get_json()
      log.debug(product_json)

      try:
        r = orm.products.update_one({"_id": ObjectId(product_json['id'])},
                                    {"$set": product_json})
        if r.modified_count > 0:
          res.message = 'Successfully updated'
        elif r.modified_count == 0:
          res.message = 'Nothing to update'
      except Exception as e:
        res.message = str(e)
        response_status = 400

    log.debug(res)
    return res, response_status

  @staticmethod
  def get_product_by_id(product_id):
    log.info('get_product_by_id')
    orm = Products()
    res = GetProductResponse()
    response_status = 200

    try:
      r = orm.products.find_one({"_id": ObjectId(product_id)})
      res.message = 'Successful'
      product = Product.from_dict(r)
      product.id = str(r['_id'])
      res.data = product.to_dict()
    except Exception as e:
      res.message = str(e)
      response_status = 400

    log.debug(res)
    return res, response_status

  @staticmethod
  def get_product_by_host_code(host_code):
    log.info('get_product_by_host_code')
    orm = Products()
    res = GetProductsResponse()
    response_status = 200

    try:
      response = orm.products.find({"host_code": host_code})
      res.message = 'Successful'

      products = []
      for r in response:
        log.debug(r)
        product = Product.from_dict(r)
        product.id = str(r['_id'])
        products.append(product)
      res.data = products
    except Exception as e:
      res.message = str(e)
      response_status = 400

    log.debug(res)
    return res, response_status

  @staticmethod
  def get_product_by_host_code_and_product_no(host_code, product_no):
    log.info('get_product_by_number')
    orm = Products()
    res = GetProductResponse()
    response_status = 200

    try:
      r = orm.products.find_one({"host_code": host_code, "product_no": product_no})
      res.message = 'Successful'
      product = Product.from_dict(r)
      product.id = str(r['_id'])
      res.data = product.to_dict()
    except Exception as e:
      res.message = str(e)
      response_status = 400

    log.debug(res)
    return res, response_status

  @staticmethod
  def delete_product_by_id(product_id):
    orm = Products()
    res = DeleteProductResponse()
    response_status = 200
    try:
      r = orm.products.delete_one({"_id": ObjectId(product_id)})
      if r.deleted_count > 0:
        res.message = 'Successfully deleted'
      else:
        response_status = 404
        res.message = 'Product not found'
    except Exception as e:
      res.message = str(e)
      response_status = 400

    log.debug(res)

    return res, response_status
