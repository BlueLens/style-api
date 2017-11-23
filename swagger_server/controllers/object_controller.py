import connexion
from swagger_server.models.get_objects_response import GetObjectsResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from orm.objects import Objects

def get_objects(file=None):
    """
    Query to search multiple objects
    
    :param file: Image file to upload (only support jpg format yet)
    :type file: werkzeug.datastructures.FileStorage

    :rtype: GetObjectsResponse
    """
    return Objects.get_objects(file)
