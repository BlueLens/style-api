# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.get_product_response import GetProductResponse
from swagger_server.models.get_products_response import GetProductsResponse
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestProductController(BaseTestCase):
    """ ProductController integration test stubs """

    def test_get_product_by_hostcode_and_product_no(self):
        """
        Test case for get_product_by_hostcode_and_product_no

        Get Product by hostCode and productNo
        """
        response = self.client.open('//products/hosts/{hostCode}/products/{productNo}'.format(hostCode='hostCode_example', productNo='productNo_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_product_by_id(self):
        """
        Test case for get_product_by_id

        Find Product by ID
        """
        response = self.client.open('//products/{productId}'.format(productId='productId_example'),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_products(self):
        """
        Test case for get_products

        Get Products by productId
        """
        query_string = [('productId', 'productId_example'),
                        ('offset', 56),
                        ('limit', 56)]
        response = self.client.open('//products',
                                    method='GET',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_products_by_image_file(self):
        """
        Test case for get_products_by_image_file

        Query to search products
        """
        query_string = [('offset', 56),
                        ('limit', 56)]
        data = dict(file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open('//products/images',
                                    method='POST',
                                    data=data,
                                    content_type='multipart/form-data',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))

    def test_get_products_by_image_id_and_object_id(self):
        """
        Test case for get_products_by_image_id_and_object_id

        Get Products by imageId and objectId
        """
        response = self.client.open('//products/images/{imageId}/objects/{objectId}'.format(imageId='imageId_example', objectId=56),
                                    method='GET')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
