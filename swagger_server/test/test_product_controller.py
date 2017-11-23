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

    def test_get_products(self):
        """
        Test case for get_products

        Query to search products
        """
        data = dict(file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open('//products',
                                    method='POST',
                                    data=data,
                                    content_type='multipart/form-data')
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
