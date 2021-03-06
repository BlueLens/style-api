# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.box_object import BoxObject  # noqa: F401,E501
from swagger_server.models.sim_image import SimImage  # noqa: F401,E501
from swagger_server import util


class GetObjectsResponseData(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, boxes: List[BoxObject]=None, image_id: str=None, images: List[SimImage]=None):  # noqa: E501
        """GetObjectsResponseData - a model defined in Swagger

        :param boxes: The boxes of this GetObjectsResponseData.  # noqa: E501
        :type boxes: List[BoxObject]
        :param image_id: The image_id of this GetObjectsResponseData.  # noqa: E501
        :type image_id: str
        :param images: The images of this GetObjectsResponseData.  # noqa: E501
        :type images: List[SimImage]
        """
        self.swagger_types = {
            'boxes': List[BoxObject],
            'image_id': str,
            'images': List[SimImage]
        }

        self.attribute_map = {
            'boxes': 'boxes',
            'image_id': 'image_id',
            'images': 'images'
        }

        self._boxes = boxes
        self._image_id = image_id
        self._images = images

    @classmethod
    def from_dict(cls, dikt) -> 'GetObjectsResponseData':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GetObjectsResponse_data of this GetObjectsResponseData.  # noqa: E501
        :rtype: GetObjectsResponseData
        """
        return util.deserialize_model(dikt, cls)

    @property
    def boxes(self) -> List[BoxObject]:
        """Gets the boxes of this GetObjectsResponseData.


        :return: The boxes of this GetObjectsResponseData.
        :rtype: List[BoxObject]
        """
        return self._boxes

    @boxes.setter
    def boxes(self, boxes: List[BoxObject]):
        """Sets the boxes of this GetObjectsResponseData.


        :param boxes: The boxes of this GetObjectsResponseData.
        :type boxes: List[BoxObject]
        """

        self._boxes = boxes

    @property
    def image_id(self) -> str:
        """Gets the image_id of this GetObjectsResponseData.


        :return: The image_id of this GetObjectsResponseData.
        :rtype: str
        """
        return self._image_id

    @image_id.setter
    def image_id(self, image_id: str):
        """Sets the image_id of this GetObjectsResponseData.


        :param image_id: The image_id of this GetObjectsResponseData.
        :type image_id: str
        """

        self._image_id = image_id

    @property
    def images(self) -> List[SimImage]:
        """Gets the images of this GetObjectsResponseData.


        :return: The images of this GetObjectsResponseData.
        :rtype: List[SimImage]
        """
        return self._images

    @images.setter
    def images(self, images: List[SimImage]):
        """Sets the images of this GetObjectsResponseData.


        :param images: The images of this GetObjectsResponseData.
        :type images: List[SimImage]
        """

        self._images = images
