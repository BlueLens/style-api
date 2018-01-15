# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.get_objects_response import GetObjectsResponse
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestPlaygroundController(BaseTestCase):
    """ PlaygroundController integration test stubs """

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
