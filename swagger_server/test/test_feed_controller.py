# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.get_feed_response import GetFeedResponse
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestFeedController(BaseTestCase):
    """ FeedController integration test stubs """

    def test_get_feeds(self):
        """
        Test case for get_feeds

        
        """
        response = self.client.open('//feeds',
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
