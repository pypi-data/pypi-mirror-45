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


class BTMetadataPropertyConfigParams(object):
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
        'default_value': 'str',
        'display_name': 'str',
        'pattern': 'str',
        'property_id': 'str',
        'required': 'bool',
        'publish_state': 'int',
        'schema_id': 'str',
        'min_length': 'int',
        'max_length': 'int',
        'min_value': 'float',
        'max_value': 'float',
        'min_date': 'datetime',
        'max_date': 'datetime',
        'min_count': 'int',
        'max_count': 'int',
        'multiline': 'bool',
        'enum_values': 'list[dict(str, str)]'
    }

    attribute_map = {
        'default_value': 'defaultValue',
        'display_name': 'displayName',
        'pattern': 'pattern',
        'property_id': 'propertyId',
        'required': 'required',
        'publish_state': 'publishState',
        'schema_id': 'schemaId',
        'min_length': 'minLength',
        'max_length': 'maxLength',
        'min_value': 'minValue',
        'max_value': 'maxValue',
        'min_date': 'minDate',
        'max_date': 'maxDate',
        'min_count': 'minCount',
        'max_count': 'maxCount',
        'multiline': 'multiline',
        'enum_values': 'enumValues'
    }

    def __init__(self, default_value=None, display_name=None, pattern=None, property_id=None, required=None, publish_state=None, schema_id=None, min_length=None, max_length=None, min_value=None, max_value=None, min_date=None, max_date=None, min_count=None, max_count=None, multiline=None, enum_values=None):  # noqa: E501
        """BTMetadataPropertyConfigParams - a model defined in OpenAPI"""  # noqa: E501

        self._default_value = None
        self._display_name = None
        self._pattern = None
        self._property_id = None
        self._required = None
        self._publish_state = None
        self._schema_id = None
        self._min_length = None
        self._max_length = None
        self._min_value = None
        self._max_value = None
        self._min_date = None
        self._max_date = None
        self._min_count = None
        self._max_count = None
        self._multiline = None
        self._enum_values = None
        self.discriminator = None

        if default_value is not None:
            self.default_value = default_value
        if display_name is not None:
            self.display_name = display_name
        if pattern is not None:
            self.pattern = pattern
        if property_id is not None:
            self.property_id = property_id
        if required is not None:
            self.required = required
        if publish_state is not None:
            self.publish_state = publish_state
        if schema_id is not None:
            self.schema_id = schema_id
        if min_length is not None:
            self.min_length = min_length
        if max_length is not None:
            self.max_length = max_length
        if min_value is not None:
            self.min_value = min_value
        if max_value is not None:
            self.max_value = max_value
        if min_date is not None:
            self.min_date = min_date
        if max_date is not None:
            self.max_date = max_date
        if min_count is not None:
            self.min_count = min_count
        if max_count is not None:
            self.max_count = max_count
        if multiline is not None:
            self.multiline = multiline
        if enum_values is not None:
            self.enum_values = enum_values

    @property
    def default_value(self):
        """Gets the default_value of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The default_value of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: str
        """
        return self._default_value

    @default_value.setter
    def default_value(self, default_value):
        """Sets the default_value of this BTMetadataPropertyConfigParams.


        :param default_value: The default_value of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: str
        """

        self._default_value = default_value

    @property
    def display_name(self):
        """Gets the display_name of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The display_name of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this BTMetadataPropertyConfigParams.


        :param display_name: The display_name of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def pattern(self):
        """Gets the pattern of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The pattern of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: str
        """
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        """Sets the pattern of this BTMetadataPropertyConfigParams.


        :param pattern: The pattern of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: str
        """

        self._pattern = pattern

    @property
    def property_id(self):
        """Gets the property_id of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The property_id of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: str
        """
        return self._property_id

    @property_id.setter
    def property_id(self, property_id):
        """Sets the property_id of this BTMetadataPropertyConfigParams.


        :param property_id: The property_id of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: str
        """

        self._property_id = property_id

    @property
    def required(self):
        """Gets the required of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The required of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: bool
        """
        return self._required

    @required.setter
    def required(self, required):
        """Sets the required of this BTMetadataPropertyConfigParams.


        :param required: The required of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: bool
        """

        self._required = required

    @property
    def publish_state(self):
        """Gets the publish_state of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The publish_state of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: int
        """
        return self._publish_state

    @publish_state.setter
    def publish_state(self, publish_state):
        """Sets the publish_state of this BTMetadataPropertyConfigParams.


        :param publish_state: The publish_state of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: int
        """

        self._publish_state = publish_state

    @property
    def schema_id(self):
        """Gets the schema_id of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The schema_id of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: str
        """
        return self._schema_id

    @schema_id.setter
    def schema_id(self, schema_id):
        """Sets the schema_id of this BTMetadataPropertyConfigParams.


        :param schema_id: The schema_id of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: str
        """

        self._schema_id = schema_id

    @property
    def min_length(self):
        """Gets the min_length of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The min_length of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: int
        """
        return self._min_length

    @min_length.setter
    def min_length(self, min_length):
        """Sets the min_length of this BTMetadataPropertyConfigParams.


        :param min_length: The min_length of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: int
        """

        self._min_length = min_length

    @property
    def max_length(self):
        """Gets the max_length of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The max_length of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: int
        """
        return self._max_length

    @max_length.setter
    def max_length(self, max_length):
        """Sets the max_length of this BTMetadataPropertyConfigParams.


        :param max_length: The max_length of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: int
        """

        self._max_length = max_length

    @property
    def min_value(self):
        """Gets the min_value of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The min_value of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: float
        """
        return self._min_value

    @min_value.setter
    def min_value(self, min_value):
        """Sets the min_value of this BTMetadataPropertyConfigParams.


        :param min_value: The min_value of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: float
        """

        self._min_value = min_value

    @property
    def max_value(self):
        """Gets the max_value of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The max_value of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: float
        """
        return self._max_value

    @max_value.setter
    def max_value(self, max_value):
        """Sets the max_value of this BTMetadataPropertyConfigParams.


        :param max_value: The max_value of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: float
        """

        self._max_value = max_value

    @property
    def min_date(self):
        """Gets the min_date of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The min_date of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: datetime
        """
        return self._min_date

    @min_date.setter
    def min_date(self, min_date):
        """Sets the min_date of this BTMetadataPropertyConfigParams.


        :param min_date: The min_date of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: datetime
        """

        self._min_date = min_date

    @property
    def max_date(self):
        """Gets the max_date of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The max_date of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: datetime
        """
        return self._max_date

    @max_date.setter
    def max_date(self, max_date):
        """Sets the max_date of this BTMetadataPropertyConfigParams.


        :param max_date: The max_date of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: datetime
        """

        self._max_date = max_date

    @property
    def min_count(self):
        """Gets the min_count of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The min_count of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: int
        """
        return self._min_count

    @min_count.setter
    def min_count(self, min_count):
        """Sets the min_count of this BTMetadataPropertyConfigParams.


        :param min_count: The min_count of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: int
        """

        self._min_count = min_count

    @property
    def max_count(self):
        """Gets the max_count of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The max_count of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: int
        """
        return self._max_count

    @max_count.setter
    def max_count(self, max_count):
        """Sets the max_count of this BTMetadataPropertyConfigParams.


        :param max_count: The max_count of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: int
        """

        self._max_count = max_count

    @property
    def multiline(self):
        """Gets the multiline of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The multiline of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: bool
        """
        return self._multiline

    @multiline.setter
    def multiline(self, multiline):
        """Sets the multiline of this BTMetadataPropertyConfigParams.


        :param multiline: The multiline of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: bool
        """

        self._multiline = multiline

    @property
    def enum_values(self):
        """Gets the enum_values of this BTMetadataPropertyConfigParams.  # noqa: E501


        :return: The enum_values of this BTMetadataPropertyConfigParams.  # noqa: E501
        :rtype: list[dict(str, str)]
        """
        return self._enum_values

    @enum_values.setter
    def enum_values(self, enum_values):
        """Sets the enum_values of this BTMetadataPropertyConfigParams.


        :param enum_values: The enum_values of this BTMetadataPropertyConfigParams.  # noqa: E501
        :type: list[dict(str, str)]
        """

        self._enum_values = enum_values

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
        if not isinstance(other, BTMetadataPropertyConfigParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
