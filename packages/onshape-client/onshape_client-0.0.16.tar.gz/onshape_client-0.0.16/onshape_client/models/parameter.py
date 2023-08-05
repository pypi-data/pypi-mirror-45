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


class Parameter(object):
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
        'name': 'str',
        '_in': 'str',
        'description': 'str',
        'required': 'bool',
        'deprecated': 'bool',
        'allow_empty_value': 'bool',
        'getref': 'str',
        'style': 'str',
        'explode': 'bool',
        'allow_reserved': 'bool',
        'schema': 'Schema',
        'examples': 'dict(str, Example)',
        'example': 'object',
        'content': 'BodyPartHeaders',
        'extensions': 'dict(str, object)'
    }

    attribute_map = {
        'name': 'name',
        '_in': 'in',
        'description': 'description',
        'required': 'required',
        'deprecated': 'deprecated',
        'allow_empty_value': 'allowEmptyValue',
        'getref': 'get$ref',
        'style': 'style',
        'explode': 'explode',
        'allow_reserved': 'allowReserved',
        'schema': 'schema',
        'examples': 'examples',
        'example': 'example',
        'content': 'content',
        'extensions': 'extensions'
    }

    def __init__(self, name=None, _in=None, description=None, required=None, deprecated=None, allow_empty_value=None, getref=None, style=None, explode=None, allow_reserved=None, schema=None, examples=None, example=None, content=None, extensions=None):  # noqa: E501
        """Parameter - a model defined in OpenAPI"""  # noqa: E501

        self._name = None
        self.__in = None
        self._description = None
        self._required = None
        self._deprecated = None
        self._allow_empty_value = None
        self._getref = None
        self._style = None
        self._explode = None
        self._allow_reserved = None
        self._schema = None
        self._examples = None
        self._example = None
        self._content = None
        self._extensions = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if _in is not None:
            self._in = _in
        if description is not None:
            self.description = description
        if required is not None:
            self.required = required
        if deprecated is not None:
            self.deprecated = deprecated
        if allow_empty_value is not None:
            self.allow_empty_value = allow_empty_value
        if getref is not None:
            self.getref = getref
        if style is not None:
            self.style = style
        if explode is not None:
            self.explode = explode
        if allow_reserved is not None:
            self.allow_reserved = allow_reserved
        if schema is not None:
            self.schema = schema
        if examples is not None:
            self.examples = examples
        if example is not None:
            self.example = example
        if content is not None:
            self.content = content
        if extensions is not None:
            self.extensions = extensions

    @property
    def name(self):
        """Gets the name of this Parameter.  # noqa: E501


        :return: The name of this Parameter.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Parameter.


        :param name: The name of this Parameter.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def _in(self):
        """Gets the _in of this Parameter.  # noqa: E501


        :return: The _in of this Parameter.  # noqa: E501
        :rtype: str
        """
        return self.__in

    @_in.setter
    def _in(self, _in):
        """Sets the _in of this Parameter.


        :param _in: The _in of this Parameter.  # noqa: E501
        :type: str
        """

        self.__in = _in

    @property
    def description(self):
        """Gets the description of this Parameter.  # noqa: E501


        :return: The description of this Parameter.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Parameter.


        :param description: The description of this Parameter.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def required(self):
        """Gets the required of this Parameter.  # noqa: E501


        :return: The required of this Parameter.  # noqa: E501
        :rtype: bool
        """
        return self._required

    @required.setter
    def required(self, required):
        """Sets the required of this Parameter.


        :param required: The required of this Parameter.  # noqa: E501
        :type: bool
        """

        self._required = required

    @property
    def deprecated(self):
        """Gets the deprecated of this Parameter.  # noqa: E501


        :return: The deprecated of this Parameter.  # noqa: E501
        :rtype: bool
        """
        return self._deprecated

    @deprecated.setter
    def deprecated(self, deprecated):
        """Sets the deprecated of this Parameter.


        :param deprecated: The deprecated of this Parameter.  # noqa: E501
        :type: bool
        """

        self._deprecated = deprecated

    @property
    def allow_empty_value(self):
        """Gets the allow_empty_value of this Parameter.  # noqa: E501


        :return: The allow_empty_value of this Parameter.  # noqa: E501
        :rtype: bool
        """
        return self._allow_empty_value

    @allow_empty_value.setter
    def allow_empty_value(self, allow_empty_value):
        """Sets the allow_empty_value of this Parameter.


        :param allow_empty_value: The allow_empty_value of this Parameter.  # noqa: E501
        :type: bool
        """

        self._allow_empty_value = allow_empty_value

    @property
    def getref(self):
        """Gets the getref of this Parameter.  # noqa: E501


        :return: The getref of this Parameter.  # noqa: E501
        :rtype: str
        """
        return self._getref

    @getref.setter
    def getref(self, getref):
        """Sets the getref of this Parameter.


        :param getref: The getref of this Parameter.  # noqa: E501
        :type: str
        """

        self._getref = getref

    @property
    def style(self):
        """Gets the style of this Parameter.  # noqa: E501


        :return: The style of this Parameter.  # noqa: E501
        :rtype: str
        """
        return self._style

    @style.setter
    def style(self, style):
        """Sets the style of this Parameter.


        :param style: The style of this Parameter.  # noqa: E501
        :type: str
        """
        allowed_values = ["matrix", "label", "form", "simple", "spaceDelimited", "pipeDelimited", "deepObject"]  # noqa: E501
        if style not in allowed_values:
            raise ValueError(
                "Invalid value for `style` ({0}), must be one of {1}"  # noqa: E501
                .format(style, allowed_values)
            )

        self._style = style

    @property
    def explode(self):
        """Gets the explode of this Parameter.  # noqa: E501


        :return: The explode of this Parameter.  # noqa: E501
        :rtype: bool
        """
        return self._explode

    @explode.setter
    def explode(self, explode):
        """Sets the explode of this Parameter.


        :param explode: The explode of this Parameter.  # noqa: E501
        :type: bool
        """

        self._explode = explode

    @property
    def allow_reserved(self):
        """Gets the allow_reserved of this Parameter.  # noqa: E501


        :return: The allow_reserved of this Parameter.  # noqa: E501
        :rtype: bool
        """
        return self._allow_reserved

    @allow_reserved.setter
    def allow_reserved(self, allow_reserved):
        """Sets the allow_reserved of this Parameter.


        :param allow_reserved: The allow_reserved of this Parameter.  # noqa: E501
        :type: bool
        """

        self._allow_reserved = allow_reserved

    @property
    def schema(self):
        """Gets the schema of this Parameter.  # noqa: E501


        :return: The schema of this Parameter.  # noqa: E501
        :rtype: Schema
        """
        return self._schema

    @schema.setter
    def schema(self, schema):
        """Sets the schema of this Parameter.


        :param schema: The schema of this Parameter.  # noqa: E501
        :type: Schema
        """

        self._schema = schema

    @property
    def examples(self):
        """Gets the examples of this Parameter.  # noqa: E501


        :return: The examples of this Parameter.  # noqa: E501
        :rtype: dict(str, Example)
        """
        return self._examples

    @examples.setter
    def examples(self, examples):
        """Sets the examples of this Parameter.


        :param examples: The examples of this Parameter.  # noqa: E501
        :type: dict(str, Example)
        """

        self._examples = examples

    @property
    def example(self):
        """Gets the example of this Parameter.  # noqa: E501


        :return: The example of this Parameter.  # noqa: E501
        :rtype: object
        """
        return self._example

    @example.setter
    def example(self, example):
        """Sets the example of this Parameter.


        :param example: The example of this Parameter.  # noqa: E501
        :type: object
        """

        self._example = example

    @property
    def content(self):
        """Gets the content of this Parameter.  # noqa: E501


        :return: The content of this Parameter.  # noqa: E501
        :rtype: BodyPartHeaders
        """
        return self._content

    @content.setter
    def content(self, content):
        """Sets the content of this Parameter.


        :param content: The content of this Parameter.  # noqa: E501
        :type: BodyPartHeaders
        """

        self._content = content

    @property
    def extensions(self):
        """Gets the extensions of this Parameter.  # noqa: E501


        :return: The extensions of this Parameter.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._extensions

    @extensions.setter
    def extensions(self, extensions):
        """Sets the extensions of this Parameter.


        :param extensions: The extensions of this Parameter.  # noqa: E501
        :type: dict(str, object)
        """

        self._extensions = extensions

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
        if not isinstance(other, Parameter):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
