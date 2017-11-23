import connexion
from swagger_server.models.get_products_response import GetProductsResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from orm.products import Products


def get_products(file=None):
    """
    Query to search products
    
    :param file: Image file to upload (only support jpg format yet)
    :type file: werkzeug.datastructures.FileStorage

    :rtype: GetProductsResponse
    """
    return Products.get_products(file)

def get_product_by_hostcode_and_product_no(hostCode, productNo):
    """
    Get Product by hostCode and productNo
    Returns Product belongs to a Host and productNo
    :param hostCode:
    :type hostCode: str
    :param productNo:
    :type productNo: str

    :rtype: GetProductResponse
    """
    return Products.get_product_by_host_code_and_product_no(hostCode, productNo)
