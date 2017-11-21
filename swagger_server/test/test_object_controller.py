# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.get_objects_response import GetObjectsResponse
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestObjectController(BaseTestCase):
    """ ObjectController integration test stubs """

    def test_get_objects(self):
        """
        Test case for get_objects

        Query to search multiple objects
        """
        data = dict(file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open('//objects',
                                    method='POST',
                                    data=data,
                                    content_type='multipart/form-data')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
