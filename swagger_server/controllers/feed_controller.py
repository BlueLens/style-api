import connexion
from swagger_server.models.get_feed_response import GetFeedResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


def get_feeds():
    """
    
    Returns Main Feeds

    :rtype: GetFeedResponse
    """
    return 'do some magic!'
