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


class BTEnterpriseReportParams(object):
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
        'id': 'str',
        'description': 'str',
        'owner_id': 'str',
        'report_id': 'str',
        'report_name': 'str',
        'group_name': 'str',
        'public_report': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'description': 'description',
        'owner_id': 'ownerId',
        'report_id': 'reportId',
        'report_name': 'reportName',
        'group_name': 'groupName',
        'public_report': 'publicReport'
    }

    def __init__(self, name=None, id=None, description=None, owner_id=None, report_id=None, report_name=None, group_name=None, public_report=None):  # noqa: E501
        """BTEnterpriseReportParams - a model defined in OpenAPI"""  # noqa: E501

        self._name = None
        self._id = None
        self._description = None
        self._owner_id = None
        self._report_id = None
        self._report_name = None
        self._group_name = None
        self._public_report = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if description is not None:
            self.description = description
        if owner_id is not None:
            self.owner_id = owner_id
        if report_id is not None:
            self.report_id = report_id
        if report_name is not None:
            self.report_name = report_name
        if group_name is not None:
            self.group_name = group_name
        if public_report is not None:
            self.public_report = public_report

    @property
    def name(self):
        """Gets the name of this BTEnterpriseReportParams.  # noqa: E501


        :return: The name of this BTEnterpriseReportParams.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this BTEnterpriseReportParams.


        :param name: The name of this BTEnterpriseReportParams.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def id(self):
        """Gets the id of this BTEnterpriseReportParams.  # noqa: E501


        :return: The id of this BTEnterpriseReportParams.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BTEnterpriseReportParams.


        :param id: The id of this BTEnterpriseReportParams.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def description(self):
        """Gets the description of this BTEnterpriseReportParams.  # noqa: E501


        :return: The description of this BTEnterpriseReportParams.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this BTEnterpriseReportParams.


        :param description: The description of this BTEnterpriseReportParams.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def owner_id(self):
        """Gets the owner_id of this BTEnterpriseReportParams.  # noqa: E501


        :return: The owner_id of this BTEnterpriseReportParams.  # noqa: E501
        :rtype: str
        """
        return self._owner_id

    @owner_id.setter
    def owner_id(self, owner_id):
        """Sets the owner_id of this BTEnterpriseReportParams.


        :param owner_id: The owner_id of this BTEnterpriseReportParams.  # noqa: E501
        :type: str
        """

        self._owner_id = owner_id

    @property
    def report_id(self):
        """Gets the report_id of this BTEnterpriseReportParams.  # noqa: E501


        :return: The report_id of this BTEnterpriseReportParams.  # noqa: E501
        :rtype: str
        """
        return self._report_id

    @report_id.setter
    def report_id(self, report_id):
        """Sets the report_id of this BTEnterpriseReportParams.


        :param report_id: The report_id of this BTEnterpriseReportParams.  # noqa: E501
        :type: str
        """

        self._report_id = report_id

    @property
    def report_name(self):
        """Gets the report_name of this BTEnterpriseReportParams.  # noqa: E501


        :return: The report_name of this BTEnterpriseReportParams.  # noqa: E501
        :rtype: str
        """
        return self._report_name

    @report_name.setter
    def report_name(self, report_name):
        """Sets the report_name of this BTEnterpriseReportParams.


        :param report_name: The report_name of this BTEnterpriseReportParams.  # noqa: E501
        :type: str
        """

        self._report_name = report_name

    @property
    def group_name(self):
        """Gets the group_name of this BTEnterpriseReportParams.  # noqa: E501


        :return: The group_name of this BTEnterpriseReportParams.  # noqa: E501
        :rtype: str
        """
        return self._group_name

    @group_name.setter
    def group_name(self, group_name):
        """Sets the group_name of this BTEnterpriseReportParams.


        :param group_name: The group_name of this BTEnterpriseReportParams.  # noqa: E501
        :type: str
        """

        self._group_name = group_name

    @property
    def public_report(self):
        """Gets the public_report of this BTEnterpriseReportParams.  # noqa: E501


        :return: The public_report of this BTEnterpriseReportParams.  # noqa: E501
        :rtype: bool
        """
        return self._public_report

    @public_report.setter
    def public_report(self, public_report):
        """Sets the public_report of this BTEnterpriseReportParams.


        :param public_report: The public_report of this BTEnterpriseReportParams.  # noqa: E501
        :type: bool
        """

        self._public_report = public_report

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
        if not isinstance(other, BTEnterpriseReportParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
