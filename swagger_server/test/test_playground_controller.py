# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.get_images_by_category_response import GetImagesByCategoryResponse  # noqa: E501
from swagger_server.models.get_images_by_keyword_response import GetImagesByKeywordResponse  # noqa: E501
from swagger_server.models.get_images_categories_counts_by_category_response import GetImagesCategoriesCountsByCategoryResponse  # noqa: E501
from swagger_server.models.get_objects_response import GetObjectsResponse  # noqa: E501
from swagger_server.models.update_image_dataset_response import UpdateImageDatasetResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPlaygroundController(BaseTestCase):
    """PlaygroundController integration test stubs"""

    def test_get_images_by_keyword(self):
        """Test case for get_images_by_keyword

        Query to search multiple objects
        """
        query_string = [('keyword', 'keyword_example'),
                        ('categoryName', 'categoryName_example'),
                        ('offset', 56),
                        ('limit', 56)]
        response = self.client.open(
            '//playgrounds/images',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_images_dataset_by_category(self):
        """Test case for get_images_dataset_by_category

        Query to search multiple objects
        """
        query_string = [('category', 'category_example'),
                        ('offset', 56),
                        ('limit', 56)]
        response = self.client.open(
            '//playgrounds/images/datasets/{source}/categories'.format(source='source_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_images_dataset_categories_counts_by_category(self):
        """Test case for get_images_dataset_categories_counts_by_category

        Query to search category counts
        """
        query_string = [('category', 'category_example')]
        response = self.client.open(
            '//playgrounds/images/datasets/{source}/categories/counts'.format(source='source_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_playground_objects_by_user_image_file(self):
        """Test case for get_playground_objects_by_user_image_file

        
        """
        data = dict(file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '//playgrounds/objects',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_images_dataset_by_ids(self):
        """Test case for update_images_dataset_by_ids

        Update image
        """
        query_string = [('ids', 'ids_example'),
                        ('valid', true)]
        response = self.client.open(
            '//playgrounds/images/datasets/{source}'.format(source='source_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
