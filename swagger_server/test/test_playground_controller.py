# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.get_images_by_keyword_response import GetImagesByKeywordResponse
from swagger_server.models.get_objects_response import GetObjectsResponse
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestPlaygroundController(BaseTestCase):
    """ PlaygroundController integration test stubs """

    def test_get_images_by_keyword(self):
        """
        Test case for get_images_by_keyword

        Query to search multiple objects
        """
        query_string = [('keyword', 'keyword_example'),
                        ('offset', 56),
                        ('limit', 56)]
        response = self.client.open('//playgrounds/images',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_playground_objects_by_user_image_file(self):
        """
        Test case for get_playground_objects_by_user_image_file

        
        """
        data = dict(file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open('//playgrounds/objects',
                                    method='POST',
                                    data=data,
                                    content_type='multipart/form-data')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
