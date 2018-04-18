# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class GetImagesCategoriesCountsByCategoryResponseData(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, total_count: str=None, valid_count: str=None, invalid_count: str=None):  # noqa: E501
        """GetImagesCategoriesCountsByCategoryResponseData - a model defined in Swagger

        :param total_count: The total_count of this GetImagesCategoriesCountsByCategoryResponseData.  # noqa: E501
        :type total_count: str
        :param valid_count: The valid_count of this GetImagesCategoriesCountsByCategoryResponseData.  # noqa: E501
        :type valid_count: str
        :param invalid_count: The invalid_count of this GetImagesCategoriesCountsByCategoryResponseData.  # noqa: E501
        :type invalid_count: str
        """
        self.swagger_types = {
            'total_count': str,
            'valid_count': str,
            'invalid_count': str
        }

        self.attribute_map = {
            'total_count': 'total_count',
            'valid_count': 'valid_count',
            'invalid_count': 'invalid_count'
        }

        self._total_count = total_count
        self._valid_count = valid_count
        self._invalid_count = invalid_count

    @classmethod
    def from_dict(cls, dikt) -> 'GetImagesCategoriesCountsByCategoryResponseData':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GetImagesCategoriesCountsByCategoryResponse_data of this GetImagesCategoriesCountsByCategoryResponseData.  # noqa: E501
        :rtype: GetImagesCategoriesCountsByCategoryResponseData
        """
        return util.deserialize_model(dikt, cls)

    @property
    def total_count(self) -> str:
        """Gets the total_count of this GetImagesCategoriesCountsByCategoryResponseData.


        :return: The total_count of this GetImagesCategoriesCountsByCategoryResponseData.
        :rtype: str
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count: str):
        """Sets the total_count of this GetImagesCategoriesCountsByCategoryResponseData.


        :param total_count: The total_count of this GetImagesCategoriesCountsByCategoryResponseData.
        :type total_count: str
        """

        self._total_count = total_count

    @property
    def valid_count(self) -> str:
        """Gets the valid_count of this GetImagesCategoriesCountsByCategoryResponseData.


        :return: The valid_count of this GetImagesCategoriesCountsByCategoryResponseData.
        :rtype: str
        """
        return self._valid_count

    @valid_count.setter
    def valid_count(self, valid_count: str):
        """Sets the valid_count of this GetImagesCategoriesCountsByCategoryResponseData.


        :param valid_count: The valid_count of this GetImagesCategoriesCountsByCategoryResponseData.
        :type valid_count: str
        """

        self._valid_count = valid_count

    @property
    def invalid_count(self) -> str:
        """Gets the invalid_count of this GetImagesCategoriesCountsByCategoryResponseData.


        :return: The invalid_count of this GetImagesCategoriesCountsByCategoryResponseData.
        :rtype: str
        """
        return self._invalid_count

    @invalid_count.setter
    def invalid_count(self, invalid_count: str):
        """Sets the invalid_count of this GetImagesCategoriesCountsByCategoryResponseData.


        :param invalid_count: The invalid_count of this GetImagesCategoriesCountsByCategoryResponseData.
        :type invalid_count: str
        """

        self._invalid_count = invalid_count
