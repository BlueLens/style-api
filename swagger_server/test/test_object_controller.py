# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.get_objects_by_image_id_response import GetObjectsByImageIdResponse  # noqa: E501
from swagger_server.models.get_objects_response import GetObjectsResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestObjectController(BaseTestCase):
    """ObjectController integration test stubs"""

    def test_get_objects_by_image_id(self):
        """Test case for get_objects_by_image_id

        Query to search multiple objects
        """
        response = self.client.open(
            '//objects/images/{imageId}'.format(imageId='imageId_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_objects_by_user_image_file(self):
        """Test case for get_objects_by_user_image_file

        Query to search objects and images
        """
        data = dict(file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '//objects',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
