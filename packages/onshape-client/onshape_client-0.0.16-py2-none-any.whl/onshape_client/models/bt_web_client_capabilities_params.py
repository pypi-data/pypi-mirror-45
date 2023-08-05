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


class BTWebClientCapabilitiesParams(object):
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
        'oes_standard_derivatives_': 'bool',
        'vendor': 'str',
        'depth_texture': 'bool',
        'renderer': 'str',
        'angle_instanced_arrays': 'bool',
        'ext_texture_filter_anisotropic': 'bool',
        'oes_element_index_uint': 'bool',
        'oes_texture_float': 'bool',
        'oes_texture_float_linear': 'bool',
        'oes_texture_half_float': 'bool',
        'oes_texture_half_float_linear': 'bool',
        'oes_vertex_array_object': 'bool',
        'compressed_texture_s3tc': 'bool',
        'draw_buffers': 'bool',
        'has3d_mouse': 'bool',
        'screen_width': 'int',
        'screen_height': 'int',
        'device_pixel_ratio': 'float'
    }

    attribute_map = {
        'oes_standard_derivatives_': 'oesStandardDerivatives_',
        'vendor': 'vendor',
        'depth_texture': 'depthTexture',
        'renderer': 'renderer',
        'angle_instanced_arrays': 'angleInstancedArrays',
        'ext_texture_filter_anisotropic': 'extTextureFilterAnisotropic',
        'oes_element_index_uint': 'oesElementIndexUint',
        'oes_texture_float': 'oesTextureFloat',
        'oes_texture_float_linear': 'oesTextureFloatLinear',
        'oes_texture_half_float': 'oesTextureHalfFloat',
        'oes_texture_half_float_linear': 'oesTextureHalfFloatLinear',
        'oes_vertex_array_object': 'oesVertexArrayObject',
        'compressed_texture_s3tc': 'compressedTextureS3tc',
        'draw_buffers': 'drawBuffers',
        'has3d_mouse': 'has3dMouse',
        'screen_width': 'screenWidth',
        'screen_height': 'screenHeight',
        'device_pixel_ratio': 'devicePixelRatio'
    }

    def __init__(self, oes_standard_derivatives_=None, vendor=None, depth_texture=None, renderer=None, angle_instanced_arrays=None, ext_texture_filter_anisotropic=None, oes_element_index_uint=None, oes_texture_float=None, oes_texture_float_linear=None, oes_texture_half_float=None, oes_texture_half_float_linear=None, oes_vertex_array_object=None, compressed_texture_s3tc=None, draw_buffers=None, has3d_mouse=None, screen_width=None, screen_height=None, device_pixel_ratio=None):  # noqa: E501
        """BTWebClientCapabilitiesParams - a model defined in OpenAPI"""  # noqa: E501

        self._oes_standard_derivatives_ = None
        self._vendor = None
        self._depth_texture = None
        self._renderer = None
        self._angle_instanced_arrays = None
        self._ext_texture_filter_anisotropic = None
        self._oes_element_index_uint = None
        self._oes_texture_float = None
        self._oes_texture_float_linear = None
        self._oes_texture_half_float = None
        self._oes_texture_half_float_linear = None
        self._oes_vertex_array_object = None
        self._compressed_texture_s3tc = None
        self._draw_buffers = None
        self._has3d_mouse = None
        self._screen_width = None
        self._screen_height = None
        self._device_pixel_ratio = None
        self.discriminator = None

        if oes_standard_derivatives_ is not None:
            self.oes_standard_derivatives_ = oes_standard_derivatives_
        if vendor is not None:
            self.vendor = vendor
        if depth_texture is not None:
            self.depth_texture = depth_texture
        if renderer is not None:
            self.renderer = renderer
        if angle_instanced_arrays is not None:
            self.angle_instanced_arrays = angle_instanced_arrays
        if ext_texture_filter_anisotropic is not None:
            self.ext_texture_filter_anisotropic = ext_texture_filter_anisotropic
        if oes_element_index_uint is not None:
            self.oes_element_index_uint = oes_element_index_uint
        if oes_texture_float is not None:
            self.oes_texture_float = oes_texture_float
        if oes_texture_float_linear is not None:
            self.oes_texture_float_linear = oes_texture_float_linear
        if oes_texture_half_float is not None:
            self.oes_texture_half_float = oes_texture_half_float
        if oes_texture_half_float_linear is not None:
            self.oes_texture_half_float_linear = oes_texture_half_float_linear
        if oes_vertex_array_object is not None:
            self.oes_vertex_array_object = oes_vertex_array_object
        if compressed_texture_s3tc is not None:
            self.compressed_texture_s3tc = compressed_texture_s3tc
        if draw_buffers is not None:
            self.draw_buffers = draw_buffers
        if has3d_mouse is not None:
            self.has3d_mouse = has3d_mouse
        if screen_width is not None:
            self.screen_width = screen_width
        if screen_height is not None:
            self.screen_height = screen_height
        if device_pixel_ratio is not None:
            self.device_pixel_ratio = device_pixel_ratio

    @property
    def oes_standard_derivatives_(self):
        """Gets the oes_standard_derivatives_ of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The oes_standard_derivatives_ of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._oes_standard_derivatives_

    @oes_standard_derivatives_.setter
    def oes_standard_derivatives_(self, oes_standard_derivatives_):
        """Sets the oes_standard_derivatives_ of this BTWebClientCapabilitiesParams.


        :param oes_standard_derivatives_: The oes_standard_derivatives_ of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._oes_standard_derivatives_ = oes_standard_derivatives_

    @property
    def vendor(self):
        """Gets the vendor of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The vendor of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: str
        """
        return self._vendor

    @vendor.setter
    def vendor(self, vendor):
        """Sets the vendor of this BTWebClientCapabilitiesParams.


        :param vendor: The vendor of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: str
        """

        self._vendor = vendor

    @property
    def depth_texture(self):
        """Gets the depth_texture of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The depth_texture of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._depth_texture

    @depth_texture.setter
    def depth_texture(self, depth_texture):
        """Sets the depth_texture of this BTWebClientCapabilitiesParams.


        :param depth_texture: The depth_texture of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._depth_texture = depth_texture

    @property
    def renderer(self):
        """Gets the renderer of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The renderer of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: str
        """
        return self._renderer

    @renderer.setter
    def renderer(self, renderer):
        """Sets the renderer of this BTWebClientCapabilitiesParams.


        :param renderer: The renderer of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: str
        """

        self._renderer = renderer

    @property
    def angle_instanced_arrays(self):
        """Gets the angle_instanced_arrays of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The angle_instanced_arrays of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._angle_instanced_arrays

    @angle_instanced_arrays.setter
    def angle_instanced_arrays(self, angle_instanced_arrays):
        """Sets the angle_instanced_arrays of this BTWebClientCapabilitiesParams.


        :param angle_instanced_arrays: The angle_instanced_arrays of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._angle_instanced_arrays = angle_instanced_arrays

    @property
    def ext_texture_filter_anisotropic(self):
        """Gets the ext_texture_filter_anisotropic of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The ext_texture_filter_anisotropic of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._ext_texture_filter_anisotropic

    @ext_texture_filter_anisotropic.setter
    def ext_texture_filter_anisotropic(self, ext_texture_filter_anisotropic):
        """Sets the ext_texture_filter_anisotropic of this BTWebClientCapabilitiesParams.


        :param ext_texture_filter_anisotropic: The ext_texture_filter_anisotropic of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._ext_texture_filter_anisotropic = ext_texture_filter_anisotropic

    @property
    def oes_element_index_uint(self):
        """Gets the oes_element_index_uint of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The oes_element_index_uint of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._oes_element_index_uint

    @oes_element_index_uint.setter
    def oes_element_index_uint(self, oes_element_index_uint):
        """Sets the oes_element_index_uint of this BTWebClientCapabilitiesParams.


        :param oes_element_index_uint: The oes_element_index_uint of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._oes_element_index_uint = oes_element_index_uint

    @property
    def oes_texture_float(self):
        """Gets the oes_texture_float of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The oes_texture_float of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._oes_texture_float

    @oes_texture_float.setter
    def oes_texture_float(self, oes_texture_float):
        """Sets the oes_texture_float of this BTWebClientCapabilitiesParams.


        :param oes_texture_float: The oes_texture_float of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._oes_texture_float = oes_texture_float

    @property
    def oes_texture_float_linear(self):
        """Gets the oes_texture_float_linear of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The oes_texture_float_linear of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._oes_texture_float_linear

    @oes_texture_float_linear.setter
    def oes_texture_float_linear(self, oes_texture_float_linear):
        """Sets the oes_texture_float_linear of this BTWebClientCapabilitiesParams.


        :param oes_texture_float_linear: The oes_texture_float_linear of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._oes_texture_float_linear = oes_texture_float_linear

    @property
    def oes_texture_half_float(self):
        """Gets the oes_texture_half_float of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The oes_texture_half_float of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._oes_texture_half_float

    @oes_texture_half_float.setter
    def oes_texture_half_float(self, oes_texture_half_float):
        """Sets the oes_texture_half_float of this BTWebClientCapabilitiesParams.


        :param oes_texture_half_float: The oes_texture_half_float of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._oes_texture_half_float = oes_texture_half_float

    @property
    def oes_texture_half_float_linear(self):
        """Gets the oes_texture_half_float_linear of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The oes_texture_half_float_linear of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._oes_texture_half_float_linear

    @oes_texture_half_float_linear.setter
    def oes_texture_half_float_linear(self, oes_texture_half_float_linear):
        """Sets the oes_texture_half_float_linear of this BTWebClientCapabilitiesParams.


        :param oes_texture_half_float_linear: The oes_texture_half_float_linear of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._oes_texture_half_float_linear = oes_texture_half_float_linear

    @property
    def oes_vertex_array_object(self):
        """Gets the oes_vertex_array_object of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The oes_vertex_array_object of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._oes_vertex_array_object

    @oes_vertex_array_object.setter
    def oes_vertex_array_object(self, oes_vertex_array_object):
        """Sets the oes_vertex_array_object of this BTWebClientCapabilitiesParams.


        :param oes_vertex_array_object: The oes_vertex_array_object of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._oes_vertex_array_object = oes_vertex_array_object

    @property
    def compressed_texture_s3tc(self):
        """Gets the compressed_texture_s3tc of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The compressed_texture_s3tc of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._compressed_texture_s3tc

    @compressed_texture_s3tc.setter
    def compressed_texture_s3tc(self, compressed_texture_s3tc):
        """Sets the compressed_texture_s3tc of this BTWebClientCapabilitiesParams.


        :param compressed_texture_s3tc: The compressed_texture_s3tc of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._compressed_texture_s3tc = compressed_texture_s3tc

    @property
    def draw_buffers(self):
        """Gets the draw_buffers of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The draw_buffers of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._draw_buffers

    @draw_buffers.setter
    def draw_buffers(self, draw_buffers):
        """Sets the draw_buffers of this BTWebClientCapabilitiesParams.


        :param draw_buffers: The draw_buffers of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._draw_buffers = draw_buffers

    @property
    def has3d_mouse(self):
        """Gets the has3d_mouse of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The has3d_mouse of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: bool
        """
        return self._has3d_mouse

    @has3d_mouse.setter
    def has3d_mouse(self, has3d_mouse):
        """Sets the has3d_mouse of this BTWebClientCapabilitiesParams.


        :param has3d_mouse: The has3d_mouse of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: bool
        """

        self._has3d_mouse = has3d_mouse

    @property
    def screen_width(self):
        """Gets the screen_width of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The screen_width of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: int
        """
        return self._screen_width

    @screen_width.setter
    def screen_width(self, screen_width):
        """Sets the screen_width of this BTWebClientCapabilitiesParams.


        :param screen_width: The screen_width of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: int
        """

        self._screen_width = screen_width

    @property
    def screen_height(self):
        """Gets the screen_height of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The screen_height of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: int
        """
        return self._screen_height

    @screen_height.setter
    def screen_height(self, screen_height):
        """Sets the screen_height of this BTWebClientCapabilitiesParams.


        :param screen_height: The screen_height of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: int
        """

        self._screen_height = screen_height

    @property
    def device_pixel_ratio(self):
        """Gets the device_pixel_ratio of this BTWebClientCapabilitiesParams.  # noqa: E501


        :return: The device_pixel_ratio of this BTWebClientCapabilitiesParams.  # noqa: E501
        :rtype: float
        """
        return self._device_pixel_ratio

    @device_pixel_ratio.setter
    def device_pixel_ratio(self, device_pixel_ratio):
        """Sets the device_pixel_ratio of this BTWebClientCapabilitiesParams.


        :param device_pixel_ratio: The device_pixel_ratio of this BTWebClientCapabilitiesParams.  # noqa: E501
        :type: float
        """

        self._device_pixel_ratio = device_pixel_ratio

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
        if not isinstance(other, BTWebClientCapabilitiesParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
