import connexion
from swagger_server.models.get_feed_response import GetFeedResponse
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime

from controller.feeds import Feeds

def get_feeds(offset=None, limit=None):
    """
    
    Returns Main Feeds

    :rtype: GetFeedResponse
    """
    return Feeds.get_feeds(offset=offset, limit=limit)
