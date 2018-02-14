# coding: utf-8

from __future__ import absolute_import
from swagger_server.models.get_images_categories_counts_by_category_response_data import GetImagesCategoriesCountsByCategoryResponseData
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class GetImagesCategoriesCountsByCategoryResponse(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, message: str=None, data: GetImagesCategoriesCountsByCategoryResponseData=None):
        """
        GetImagesCategoriesCountsByCategoryResponse - a model defined in Swagger

        :param message: The message of this GetImagesCategoriesCountsByCategoryResponse.
        :type message: str
        :param data: The data of this GetImagesCategoriesCountsByCategoryResponse.
        :type data: GetImagesCategoriesCountsByCategoryResponseData
        """
        self.swagger_types = {
            'message': str,
            'data': GetImagesCategoriesCountsByCategoryResponseData
        }

        self.attribute_map = {
            'message': 'message',
            'data': 'data'
        }

        self._message = message
        self._data = data

    @classmethod
    def from_dict(cls, dikt) -> 'GetImagesCategoriesCountsByCategoryResponse':
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GetImagesCategoriesCountsByCategoryResponse of this GetImagesCategoriesCountsByCategoryResponse.
        :rtype: GetImagesCategoriesCountsByCategoryResponse
        """
        return deserialize_model(dikt, cls)

    @property
    def message(self) -> str:
        """
        Gets the message of this GetImagesCategoriesCountsByCategoryResponse.

        :return: The message of this GetImagesCategoriesCountsByCategoryResponse.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """
        Sets the message of this GetImagesCategoriesCountsByCategoryResponse.

        :param message: The message of this GetImagesCategoriesCountsByCategoryResponse.
        :type message: str
        """

        self._message = message

    @property
    def data(self) -> GetImagesCategoriesCountsByCategoryResponseData:
        """
        Gets the data of this GetImagesCategoriesCountsByCategoryResponse.

        :return: The data of this GetImagesCategoriesCountsByCategoryResponse.
        :rtype: GetImagesCategoriesCountsByCategoryResponseData
        """
        return self._data

    @data.setter
    def data(self, data: GetImagesCategoriesCountsByCategoryResponseData):
        """
        Sets the data of this GetImagesCategoriesCountsByCategoryResponse.

        :param data: The data of this GetImagesCategoriesCountsByCategoryResponse.
        :type data: GetImagesCategoriesCountsByCategoryResponseData
        """

        self._data = data

