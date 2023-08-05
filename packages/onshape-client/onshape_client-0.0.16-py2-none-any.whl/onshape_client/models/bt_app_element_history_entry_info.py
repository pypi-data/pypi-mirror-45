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


class BTAppElementHistoryEntryInfo(object):
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
        'description': 'str',
        'created_at': 'datetime',
        'change_id': 'str'
    }

    attribute_map = {
        'description': 'description',
        'created_at': 'createdAt',
        'change_id': 'changeId'
    }

    def __init__(self, description=None, created_at=None, change_id=None):  # noqa: E501
        """BTAppElementHistoryEntryInfo - a model defined in OpenAPI"""  # noqa: E501

        self._description = None
        self._created_at = None
        self._change_id = None
        self.discriminator = None

        if description is not None:
            self.description = description
        if created_at is not None:
            self.created_at = created_at
        if change_id is not None:
            self.change_id = change_id

    @property
    def description(self):
        """Gets the description of this BTAppElementHistoryEntryInfo.  # noqa: E501


        :return: The description of this BTAppElementHistoryEntryInfo.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this BTAppElementHistoryEntryInfo.


        :param description: The description of this BTAppElementHistoryEntryInfo.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def created_at(self):
        """Gets the created_at of this BTAppElementHistoryEntryInfo.  # noqa: E501


        :return: The created_at of this BTAppElementHistoryEntryInfo.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this BTAppElementHistoryEntryInfo.


        :param created_at: The created_at of this BTAppElementHistoryEntryInfo.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def change_id(self):
        """Gets the change_id of this BTAppElementHistoryEntryInfo.  # noqa: E501


        :return: The change_id of this BTAppElementHistoryEntryInfo.  # noqa: E501
        :rtype: str
        """
        return self._change_id

    @change_id.setter
    def change_id(self, change_id):
        """Sets the change_id of this BTAppElementHistoryEntryInfo.


        :param change_id: The change_id of this BTAppElementHistoryEntryInfo.  # noqa: E501
        :type: str
        """

        self._change_id = change_id

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
        if not isinstance(other, BTAppElementHistoryEntryInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
