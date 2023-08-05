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


class BTDiffInfo(object):
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
        'type': 'str',
        'source_id': 'str',
        'collection_changes': 'dict(str, list[BTDiffInfo])',
        'target_id': 'str',
        'source_value': 'str',
        'target_value': 'str'
    }

    attribute_map = {
        'type': 'type',
        'source_id': 'sourceId',
        'collection_changes': 'collectionChanges',
        'target_id': 'targetId',
        'source_value': 'sourceValue',
        'target_value': 'targetValue'
    }

    def __init__(self, type=None, source_id=None, collection_changes=None, target_id=None, source_value=None, target_value=None):  # noqa: E501
        """BTDiffInfo - a model defined in OpenAPI"""  # noqa: E501

        self._type = None
        self._source_id = None
        self._collection_changes = None
        self._target_id = None
        self._source_value = None
        self._target_value = None
        self.discriminator = None

        if type is not None:
            self.type = type
        if source_id is not None:
            self.source_id = source_id
        if collection_changes is not None:
            self.collection_changes = collection_changes
        if target_id is not None:
            self.target_id = target_id
        if source_value is not None:
            self.source_value = source_value
        if target_value is not None:
            self.target_value = target_value

    @property
    def type(self):
        """Gets the type of this BTDiffInfo.  # noqa: E501


        :return: The type of this BTDiffInfo.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this BTDiffInfo.


        :param type: The type of this BTDiffInfo.  # noqa: E501
        :type: str
        """
        allowed_values = ["NONE", "MOVED", "MODIFIED", "MOVED_AND_MODIFIED", "ADDED", "DELETED", "UNKNOWN"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def source_id(self):
        """Gets the source_id of this BTDiffInfo.  # noqa: E501


        :return: The source_id of this BTDiffInfo.  # noqa: E501
        :rtype: str
        """
        return self._source_id

    @source_id.setter
    def source_id(self, source_id):
        """Sets the source_id of this BTDiffInfo.


        :param source_id: The source_id of this BTDiffInfo.  # noqa: E501
        :type: str
        """

        self._source_id = source_id

    @property
    def collection_changes(self):
        """Gets the collection_changes of this BTDiffInfo.  # noqa: E501


        :return: The collection_changes of this BTDiffInfo.  # noqa: E501
        :rtype: dict(str, list[BTDiffInfo])
        """
        return self._collection_changes

    @collection_changes.setter
    def collection_changes(self, collection_changes):
        """Sets the collection_changes of this BTDiffInfo.


        :param collection_changes: The collection_changes of this BTDiffInfo.  # noqa: E501
        :type: dict(str, list[BTDiffInfo])
        """

        self._collection_changes = collection_changes

    @property
    def target_id(self):
        """Gets the target_id of this BTDiffInfo.  # noqa: E501


        :return: The target_id of this BTDiffInfo.  # noqa: E501
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """Sets the target_id of this BTDiffInfo.


        :param target_id: The target_id of this BTDiffInfo.  # noqa: E501
        :type: str
        """

        self._target_id = target_id

    @property
    def source_value(self):
        """Gets the source_value of this BTDiffInfo.  # noqa: E501


        :return: The source_value of this BTDiffInfo.  # noqa: E501
        :rtype: str
        """
        return self._source_value

    @source_value.setter
    def source_value(self, source_value):
        """Sets the source_value of this BTDiffInfo.


        :param source_value: The source_value of this BTDiffInfo.  # noqa: E501
        :type: str
        """

        self._source_value = source_value

    @property
    def target_value(self):
        """Gets the target_value of this BTDiffInfo.  # noqa: E501


        :return: The target_value of this BTDiffInfo.  # noqa: E501
        :rtype: str
        """
        return self._target_value

    @target_value.setter
    def target_value(self, target_value):
        """Sets the target_value of this BTDiffInfo.


        :param target_value: The target_value of this BTDiffInfo.  # noqa: E501
        :type: str
        """

        self._target_value = target_value

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
        if not isinstance(other, BTDiffInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
