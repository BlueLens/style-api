# coding: utf-8

from __future__ import absolute_import
from swagger_server.models.get_images_by_category_response_data import GetImagesByCategoryResponseData
from .base_model_ import Model
from datetime import date, datetime
from typing import List, Dict
from ..util import deserialize_model


class GetImagesByCategoryResponse(Model):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, message: str=None, data: GetImagesByCategoryResponseData=None):
        """
        GetImagesByCategoryResponse - a model defined in Swagger

        :param message: The message of this GetImagesByCategoryResponse.
        :type message: str
        :param data: The data of this GetImagesByCategoryResponse.
        :type data: GetImagesByCategoryResponseData
        """
        self.swagger_types = {
            'message': str,
            'data': GetImagesByCategoryResponseData
        }

        self.attribute_map = {
            'message': 'message',
            'data': 'data'
        }

        self._message = message
        self._data = data

    @classmethod
    def from_dict(cls, dikt) -> 'GetImagesByCategoryResponse':
        """
        Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GetImagesByCategoryResponse of this GetImagesByCategoryResponse.
        :rtype: GetImagesByCategoryResponse
        """
        return deserialize_model(dikt, cls)

    @property
    def message(self) -> str:
        """
        Gets the message of this GetImagesByCategoryResponse.

        :return: The message of this GetImagesByCategoryResponse.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """
        Sets the message of this GetImagesByCategoryResponse.

        :param message: The message of this GetImagesByCategoryResponse.
        :type message: str
        """

        self._message = message

    @property
    def data(self) -> GetImagesByCategoryResponseData:
        """
        Gets the data of this GetImagesByCategoryResponse.

        :return: The data of this GetImagesByCategoryResponse.
        :rtype: GetImagesByCategoryResponseData
        """
        return self._data

    @data.setter
    def data(self, data: GetImagesByCategoryResponseData):
        """
        Sets the data of this GetImagesByCategoryResponse.

        :param data: The data of this GetImagesByCategoryResponse.
        :type data: GetImagesByCategoryResponseData
        """

        self._data = data
