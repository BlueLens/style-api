import connexion
from swagger_server.models.get_products_response import GetProductsResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from controller.products import Products


def get_products(file=None):
    """
    Query to search products
    
    :param file: Image file to upload (only support jpg format yet)
    :type file: werkzeug.datastructures.FileStorage

    :rtype: GetProductsResponse
    """
    return Products.get_products(file)

def get_products_by_image_id_and_object_id(imageId, objectId):
    """
    Get Products by imageId and objectId
    Returns Products belongs to a imageId and objectId
    :param imageId:
    :type imageId: str
    :param objectId:
    :type objectId: int

    :rtype: GetProductsResponse
    """
    return Products.get_products_by_image_id_and_object_id(imageId, objectId)

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

def get_product_by_id(productId):
    """
    Find Product by ID
    Returns a single Product
    :param productId: ID of Product to return
    :type productId: str

    :rtype: GetProductResponse
    """
    return Products.get_product_by_id(productId)
