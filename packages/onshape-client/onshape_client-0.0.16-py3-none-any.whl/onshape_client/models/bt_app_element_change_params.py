# coding: utf-8

"""
    Onshape REST API

    The Onshape REST API consumed by all clients.  # noqa: E501

    OpenAPI spec version: 1.96
    Contact: api-support@onshape.zendesk.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class BTAppElementChangeParams(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'subelement_id': 'str',
        'base_content': 'str',
        'delta': 'str'
    }

    attribute_map = {
        'subelement_id': 'subelementId',
        'base_content': 'baseContent',
        'delta': 'delta'
    }

    def __init__(self, subelement_id=None, base_content=None, delta=None):  # noqa: E501
        """BTAppElementChangeParams - a model defined in OpenAPI"""  # noqa: E501

        self._subelement_id = None
        self._base_content = None
        self._delta = None
        self.discriminator = None

        if subelement_id is not None:
            self.subelement_id = subelement_id
        if base_content is not None:
            self.base_content = base_content
        if delta is not None:
            self.delta = delta

    @property
    def subelement_id(self):
        """Gets the subelement_id of this BTAppElementChangeParams.  # noqa: E501


        :return: The subelement_id of this BTAppElementChangeParams.  # noqa: E501
        :rtype: str
        """
        return self._subelement_id

    @subelement_id.setter
    def subelement_id(self, subelement_id):
        """Sets the subelement_id of this BTAppElementChangeParams.


        :param subelement_id: The subelement_id of this BTAppElementChangeParams.  # noqa: E501
        :type: str
        """

        self._subelement_id = subelement_id

    @property
    def base_content(self):
        """Gets the base_content of this BTAppElementChangeParams.  # noqa: E501


        :return: The base_content of this BTAppElementChangeParams.  # noqa: E501
        :rtype: str
        """
        return self._base_content

    @base_content.setter
    def base_content(self, base_content):
        """Sets the base_content of this BTAppElementChangeParams.


        :param base_content: The base_content of this BTAppElementChangeParams.  # noqa: E501
        :type: str
        """

        self._base_content = base_content

    @property
    def delta(self):
        """Gets the delta of this BTAppElementChangeParams.  # noqa: E501


        :return: The delta of this BTAppElementChangeParams.  # noqa: E501
        :rtype: str
        """
        return self._delta

    @delta.setter
    def delta(self, delta):
        """Sets the delta of this BTAppElementChangeParams.


        :param delta: The delta of this BTAppElementChangeParams.  # noqa: E501
        :type: str
        """

        self._delta = delta

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BTAppElementChangeParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
