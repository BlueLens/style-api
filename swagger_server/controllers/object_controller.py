import connexion
from swagger_server.models.get_objects_by_image_id_response import GetObjectsByImageIdResponse
from swagger_server.models.get_objects_response import GetObjectsResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from controller.objects import Objects

def get_objects_by_image_id(imageId):
    """
    Query to search multiple objects

    :param imageId:
    :type imageId: str

    :rtype: GetObjectsByImageIdResponse
    """
    return Objects.get_objects_by_image_id(imageId)

def get_objects_by_user_image_file(file):
    """
    Query to search objects and products

    :param file: User's Image file to upload (only support jpg format yet)
    :type file: werkzeug.datastructures.FileStorage

    :rtype: GetObjectsResponse
    """
    return Objects.get_objects_by_user_image_file(file)

