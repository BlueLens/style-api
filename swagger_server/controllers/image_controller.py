import connexion
from swagger_server.models.get_images_response import GetImagesResponse
from swagger_server.models.get_image_response import GetImageResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from controller.images import Images

def get_images_by_user_image_file(file=None, offset=0, limit=5):
    """
    Query to search images

    :param file: User's Image file to upload (only support jpg format yet)
    :type file: werkzeug.datastructures.FileStorage
    :param offset:
    :type offset: int
    :param limit:
    :type limit: int

    :rtype: GetImagesResponse
    """
    return Images.get_images_by_user_image_file(file, offset, limit)

def get_images(imageId, offset=0, limit=10):
    """
    Get Images by imageId
    Returns similar Images with imageId
    :param imageId:
    :type imageId: str
    :param offset:
    :type offset: int
    :param limit:
    :type limit: int

    :rtype: GetImagesResponse
    """
    return Images.get_images(imageId, offset, limit)

def get_images_by_user_image_id_and_object_index(userImageId, objectIndex):
    """
    Get Images by imageId and objectId
    Returns Images belongs to a imageId and objectId
    :param imageId:
    :type imageId: str
    :param objectId:
    :type objectId: int

    :rtype: GetImagesResponse
    """
    return Images.get_images_by_user_image_id_and_object_index(userImageId, objectIndex)

def get_image_by_hostcode_and_product_no(hostCode, productNo):
    """
    Get Image by hostCode and productNo
    Returns Pmage belongs to a Host and productNo
    :param hostCode:
    :type hostCode: str
    :param productNo:
    :type productNo: str

    :rtype: GetImageResponse
    """
    return Images.get_image_by_host_code_and_product_no(hostCode, productNo)

def get_image_by_id(imageId):
    """
    Find Image by ID
    Returns a single Image
    :param imageId: ID of Image to return
    :type imageId: str

    :rtype: GetImageResponse
    """
    return Images.get_image_by_id(imageId)

def get_images_by_object_id(objectId, offset=0, limit=10):
    """
    Query to search images by object id

    :param objectId:
    :type objectId: str

    :rtype: GetImagesResponse
    """
    return Images.get_images_by_object_id(objectId, offset=offset, limit=limit)
