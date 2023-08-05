# coding: utf-8

"""
    Onshape REST API

    The Onshape REST API consumed by all clients.  # noqa: E501

    OpenAPI spec version: 1.96
    Contact: api-support@onshape.zendesk.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from onshape_client.api_client import ApiClient


class TranslationsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_translation(self, did, wid, **kwargs):  # noqa: E501
        """create_translation  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_translation(did, wid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str did: (required)
        :param str wid: (required)
        :param ContentDisposition content_disposition:
        :param object entity:
        :param BodyPartHeaders headers:
        :param BodyPartMediaType media_type:
        :param MessageBodyWorkers message_body_workers:
        :param MultiPart parent:
        :param object providers:
        :param list[BodyPart] body_parts:
        :param BodyPartHeaders parameterized_headers:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_translation_with_http_info(did, wid, **kwargs)  # noqa: E501
        else:
            (data) = self.create_translation_with_http_info(did, wid, **kwargs)  # noqa: E501
            return data

    def create_translation_with_http_info(self, did, wid, **kwargs):  # noqa: E501
        """create_translation  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_translation_with_http_info(did, wid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str did: (required)
        :param str wid: (required)
        :param ContentDisposition content_disposition:
        :param object entity:
        :param BodyPartHeaders headers:
        :param BodyPartMediaType media_type:
        :param MessageBodyWorkers message_body_workers:
        :param MultiPart parent:
        :param object providers:
        :param list[BodyPart] body_parts:
        :param BodyPartHeaders parameterized_headers:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['did', 'wid', 'content_disposition', 'entity', 'headers', 'media_type', 'message_body_workers', 'parent', 'providers', 'body_parts', 'parameterized_headers']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_translation" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'did' is set
        if ('did' not in local_var_params or
                local_var_params['did'] is None):
            raise ValueError("Missing the required parameter `did` when calling `create_translation`")  # noqa: E501
        # verify the required parameter 'wid' is set
        if ('wid' not in local_var_params or
                local_var_params['wid'] is None):
            raise ValueError("Missing the required parameter `wid` when calling `create_translation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'did' in local_var_params:
            path_params['did'] = local_var_params['did']  # noqa: E501
        if 'wid' in local_var_params:
            path_params['wid'] = local_var_params['wid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'content_disposition' in local_var_params:
            form_params.append(('contentDisposition', local_var_params['content_disposition']))  # noqa: E501
        if 'entity' in local_var_params:
            form_params.append(('entity', local_var_params['entity']))  # noqa: E501
        if 'headers' in local_var_params:
            form_params.append(('headers', local_var_params['headers']))  # noqa: E501
        if 'media_type' in local_var_params:
            form_params.append(('mediaType', local_var_params['media_type']))  # noqa: E501
        if 'message_body_workers' in local_var_params:
            form_params.append(('messageBodyWorkers', local_var_params['message_body_workers']))  # noqa: E501
        if 'parent' in local_var_params:
            form_params.append(('parent', local_var_params['parent']))  # noqa: E501
        if 'providers' in local_var_params:
            form_params.append(('providers', local_var_params['providers']))  # noqa: E501
        if 'body_parts' in local_var_params:
            form_params.append(('bodyParts', local_var_params['body_parts']))  # noqa: E501
            collection_formats['bodyParts'] = 'csv'  # noqa: E501
        if 'parameterized_headers' in local_var_params:
            form_params.append(('parameterizedHeaders', local_var_params['parameterized_headers']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.onshape.v1+json;charset=UTF-8; qs=0.1', 'application/json;charset=UTF-8; qs=0.9'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2']  # noqa: E501

        return self.api_client.call_api(
            '/api/translations/d/{did}/w/{wid}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_translation(self, tid, **kwargs):  # noqa: E501
        """delete_translation  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_translation(tid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str tid: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_translation_with_http_info(tid, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_translation_with_http_info(tid, **kwargs)  # noqa: E501
            return data

    def delete_translation_with_http_info(self, tid, **kwargs):  # noqa: E501
        """delete_translation  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_translation_with_http_info(tid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str tid: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['tid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_translation" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'tid' is set
        if ('tid' not in local_var_params or
                local_var_params['tid'] is None):
            raise ValueError("Missing the required parameter `tid` when calling `delete_translation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'tid' in local_var_params:
            path_params['tid'] = local_var_params['tid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.onshape.v1+json;charset=UTF-8; qs=0.1', 'application/json;charset=UTF-8; qs=0.9'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2']  # noqa: E501

        return self.api_client.call_api(
            '/api/translations/{tid}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_document_translations(self, did, **kwargs):  # noqa: E501
        """get_document_translations  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_document_translations(did, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str did: (required)
        :param int offset:
        :param int limit:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_document_translations_with_http_info(did, **kwargs)  # noqa: E501
        else:
            (data) = self.get_document_translations_with_http_info(did, **kwargs)  # noqa: E501
            return data

    def get_document_translations_with_http_info(self, did, **kwargs):  # noqa: E501
        """get_document_translations  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_document_translations_with_http_info(did, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str did: (required)
        :param int offset:
        :param int limit:
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['did', 'offset', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_document_translations" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'did' is set
        if ('did' not in local_var_params or
                local_var_params['did'] is None):
            raise ValueError("Missing the required parameter `did` when calling `get_document_translations`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'did' in local_var_params:
            path_params['did'] = local_var_params['did']  # noqa: E501

        query_params = []
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.onshape.v1+json;charset=UTF-8; qs=0.1', 'application/json;charset=UTF-8; qs=0.9'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2']  # noqa: E501

        return self.api_client.call_api(
            '/api/translations/d/{did}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_translation(self, tid, **kwargs):  # noqa: E501
        """get_translation  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_translation(tid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str tid: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_translation_with_http_info(tid, **kwargs)  # noqa: E501
        else:
            (data) = self.get_translation_with_http_info(tid, **kwargs)  # noqa: E501
            return data

    def get_translation_with_http_info(self, tid, **kwargs):  # noqa: E501
        """get_translation  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_translation_with_http_info(tid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str tid: (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['tid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_translation" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'tid' is set
        if ('tid' not in local_var_params or
                local_var_params['tid'] is None):
            raise ValueError("Missing the required parameter `tid` when calling `get_translation`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'tid' in local_var_params:
            path_params['tid'] = local_var_params['tid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.onshape.v1+json;charset=UTF-8; qs=0.1', 'application/json;charset=UTF-8; qs=0.9'])  # noqa: E501

        # Authentication setting
        auth_settings = ['OAuth2']  # noqa: E501

        return self.api_client.call_api(
            '/api/translations/{tid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_translator_formats5(self, **kwargs):  # noqa: E501
        """get_translator_formats5  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_translator_formats5(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_translator_formats5_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_translator_formats5_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_translator_formats5_with_http_info(self, **kwargs):  # noqa: E501
        """get_translator_formats5  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_translator_formats5_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_translator_formats5" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/vnd.onshape.v1+json;charset=UTF-8; qs=0.1', 'application/json;charset=UTF-8; qs=0.9'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/api/translations/translationformats', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
