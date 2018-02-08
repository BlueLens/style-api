import connexion
from swagger_server.models.get_objects_response import GetObjectsResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from controller.playgrounds import Playgrounds

def get_images_by_keyword(keyword=None, offset=None, limit=None):
    """
    Query to search multiple objects

    :param keyword:
    :type keyword: str
    :param offset:
    :type offset: int
    :param limit:
    :type limit: int

    :rtype: GetImagesByKeywordResponse
    """
    return Playgrounds.get_playground_images_by_keyword(keyword, offset=offset, limit=limit)

def get_images_dataset_by_category(source, category=None, offset=None, limit=None):
    """
    Query to search multiple objects

    :param source:
    :type source: str
    :param category:
    :type category: str
    :param offset:
    :type offset: int
    :param limit:
    :type limit: int

    :rtype: GetImagesByCategoryResponse
    """
    return Playgrounds.get_playground_images_by_category(source, category=category, offset=offset, limit=limit)

def get_playground_objects_by_user_image_file(file):
    """
    
    
    :param file: User&#39;s Image file to upload (only support jpg format yet)
    :type file: werkzeug.datastructures.FileStorage

    :rtype: GetObjectsResponse
    """
    return Playgrounds.get_playground_objects_by_user_image_file(file)

def update_images_dataset_by_ids(source, ids, valid):
    """
    Update image

    :param source:
    :type source: str
    :param ids:
    :type ids: List[str]
    :param valid:
    :type valid: bool

    :rtype: UpdateImageDatasetResponse
    """
    return Playgrounds.update_images_dataset_by_ids(source, ids, valid)
