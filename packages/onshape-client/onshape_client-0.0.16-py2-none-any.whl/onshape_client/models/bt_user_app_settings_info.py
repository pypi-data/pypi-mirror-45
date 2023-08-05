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


class BTUserAppSettingsInfo(object):
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
        'settings': 'list[BTSettingInfo]'
    }

    attribute_map = {
        'settings': 'settings'
    }

    def __init__(self, settings=None):  # noqa: E501
        """BTUserAppSettingsInfo - a model defined in OpenAPI"""  # noqa: E501

        self._settings = None
        self.discriminator = None

        if settings is not None:
            self.settings = settings

    @property
    def settings(self):
        """Gets the settings of this BTUserAppSettingsInfo.  # noqa: E501


        :return: The settings of this BTUserAppSettingsInfo.  # noqa: E501
        :rtype: list[BTSettingInfo]
        """
        return self._settings

    @settings.setter
    def settings(self, settings):
        """Sets the settings of this BTUserAppSettingsInfo.


        :param settings: The settings of this BTUserAppSettingsInfo.  # noqa: E501
        :type: list[BTSettingInfo]
        """

        self._settings = settings

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
        if not isinstance(other, BTUserAppSettingsInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
