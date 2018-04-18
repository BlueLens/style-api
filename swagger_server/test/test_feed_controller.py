# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.get_feed_response import GetFeedResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestFeedController(BaseTestCase):
    """FeedController integration test stubs"""

    def test_get_feeds(self):
        """Test case for get_feeds

        
        """
        query_string = [('offset', 56),
                        ('limit', 56)]
        response = self.client.open(
            '//feeds',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
