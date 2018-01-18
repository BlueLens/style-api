# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.get_image_response import GetImageResponse
from swagger_server.models.get_images_response import GetImagesResponse
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestImageController(BaseTestCase):
    """ ImageController integration test stubs """

    def test_get_image_by_hostcode_and_product_no(self):
        """
        Test case for get_image_by_hostcode_and_product_no

        Get Image by hostCode and productNo
        """
        response = self.client.open('//images/hosts/{hostCode}/images/{productNo}'.format(hostCode='hostCode_example', productNo='productNo_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_image_by_id(self):
        """
        Test case for get_image_by_id

        Find Images by ID
        """
        response = self.client.open('//images/{imageId}'.format(imageId='imageId_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_images(self):
        """
        Test case for get_images

        Get Images by imageId
        """
        query_string = [('imageId', 'imageId_example'),
                        ('offset', 56),
                        ('limit', 56)]
        response = self.client.open('//images',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_images_by_object_id(self):
        """
        Test case for get_images_by_object_id

        Query to search images by object id
        """
        response = self.client.open('//images/objects/{objectId}'.format(objectId='objectId_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_images_by_user_image_file(self):
        """
        Test case for get_images_by_user_image_file

        Query to search images
        """
        query_string = [('offset', 56),
                        ('limit', 56)]
        data = dict(file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open('//images/userImages',
                                    method='POST',
                                    data=data,
                                    content_type='multipart/form-data',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_images_by_user_image_id_and_object_index(self):
        """
        Test case for get_images_by_user_image_id_and_object_index

        Get Images by userImageId and objectIndex
        """
        response = self.client.open('//images/userImages/{userImageId}/objects/{objectIndex}'.format(userImageId='userImageId_example', objectIndex=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
