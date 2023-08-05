# coding: utf-8

"""
    Fortanix SDKMS REST API

    This is a set of REST APIs for accessing the Fortanix Self-Defending Key Management System. This includes APIs for managing accounts, and for performing cryptographic and key management operations. 

    OpenAPI spec version: 1.0.0-20181211
    Contact: support@fortanix.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""


from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..api_client import ApiClient


# NOTE: This class is auto generated by the swagger code generator program.
# Do not edit the class manually.
# Ref: https://github.com/swagger-api/swagger-codegen
class SignAndVerifyApi(object):
    """
    @undocumented: batch_sign_with_http_info
    @undocumented: batch_verify_with_http_info
    @undocumented: sign_with_http_info
    @undocumented: sign_ex_with_http_info
    @undocumented: verify_with_http_info
    @undocumented: verify_ex_with_http_info
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def batch_sign(self, body, async=False, **kwargs):
        """
        The data to be signed and the key ids to be used are provided in the request body. The signature is returned in the response body. The ordering of the body matches the ordering of the request. An individual status code is returned for each batch item. Maximum size of the entire batch request is 512 KB. 
        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{BatchSignRequest}
        @param body: Batch Sign request (required)
        @rtype: L{BatchSignResponse}
        @return:
        
        If the method is called asynchronously, returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if async:
            return self.batch_sign_with_http_info(body, async=async, **kwargs)
        else:
            (data) = self.batch_sign_with_http_info(body, async=async, **kwargs)
            return data

    def batch_sign_with_http_info(self, body, async=False, **kwargs):
        """
        The data to be signed and the key ids to be used are provided in the request body. The signature is returned in the response body. The ordering of the body matches the ordering of the request. An individual status code is returned for each batch item. Maximum size of the entire batch request is 512 KB. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True::
            >>> thread = api.batch_sign_with_http_info(body, async=True)
            >>> result = thread.get()

        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{BatchSignRequest}
        @param body: Batch Sign request (required)
        @rtype: L{BatchSignResponse}
        @return:

        If the method is called asynchronously, returns the request thread.
        """

        all_params = ['body']
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method batch_sign" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `batch_sign`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['bearerToken']

        return self.api_client.call_api('/crypto/v1/keys/batch/sign', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BatchSignResponse',
                                        auth_settings=auth_settings,
                                        async=params.get('async'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def batch_verify(self, body, async=False, **kwargs):
        """
        The signature to be verified and the key ids to be used are provided in the request body. The result (true of false) returned in the response body. The ordering of the body matches the ordering of the request. An individual status code is returned for each batch item. Maximum size of the entire batch request is 512 KB. 
        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{BatchVerifyRequest}
        @param body: Batch Verify request (required)
        @rtype: L{BatchVerifyResponse}
        @return:
        
        If the method is called asynchronously, returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if async:
            return self.batch_verify_with_http_info(body, async=async, **kwargs)
        else:
            (data) = self.batch_verify_with_http_info(body, async=async, **kwargs)
            return data

    def batch_verify_with_http_info(self, body, async=False, **kwargs):
        """
        The signature to be verified and the key ids to be used are provided in the request body. The result (true of false) returned in the response body. The ordering of the body matches the ordering of the request. An individual status code is returned for each batch item. Maximum size of the entire batch request is 512 KB. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True::
            >>> thread = api.batch_verify_with_http_info(body, async=True)
            >>> result = thread.get()

        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{BatchVerifyRequest}
        @param body: Batch Verify request (required)
        @rtype: L{BatchVerifyResponse}
        @return:

        If the method is called asynchronously, returns the request thread.
        """

        all_params = ['body']
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method batch_verify" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `batch_verify`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['bearerToken']

        return self.api_client.call_api('/crypto/v1/keys/batch/verify', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='BatchVerifyResponse',
                                        auth_settings=auth_settings,
                                        async=params.get('async'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def sign(self, key_id, body, async=False, **kwargs):
        """
        Sign data with a private key. The signing key must be an asymmetric key with the private part present. The sign operation must be enabled for this key. Symmetric keys  may not be used to sign data. They can be used with the computeMac and verifyMac methods. <br> The data must be hashed with a SHA-1 or SHA-2 family hash algorithm. 
        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type key_id: L{str}
        @param key_id: kid of security object (required)
        @type body: L{SignRequest}
        @param body: Signature request (required)
        @rtype: L{SignResponse}
        @return:
        
        If the method is called asynchronously, returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if async:
            return self.sign_with_http_info(key_id, body, async=async, **kwargs)
        else:
            (data) = self.sign_with_http_info(key_id, body, async=async, **kwargs)
            return data

    def sign_with_http_info(self, key_id, body, async=False, **kwargs):
        """
        Sign data with a private key. The signing key must be an asymmetric key with the private part present. The sign operation must be enabled for this key. Symmetric keys  may not be used to sign data. They can be used with the computeMac and verifyMac methods. <br> The data must be hashed with a SHA-1 or SHA-2 family hash algorithm. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True::
            >>> thread = api.sign_with_http_info(key_id, body, async=True)
            >>> result = thread.get()

        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type key_id: L{str}
        @param key_id: kid of security object (required)
        @type body: L{SignRequest}
        @param body: Signature request (required)
        @rtype: L{SignResponse}
        @return:

        If the method is called asynchronously, returns the request thread.
        """

        all_params = ['key_id', 'body']
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sign" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'key_id' is set
        if ('key_id' not in params) or (params['key_id'] is None):
            raise ValueError("Missing the required parameter `key_id` when calling `sign`")
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `sign`")


        collection_formats = {}

        path_params = {}
        if 'key_id' in params:
            path_params['key-id'] = params['key_id']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['bearerToken']

        return self.api_client.call_api('/crypto/v1/keys/{key-id}/sign', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='SignResponse',
                                        auth_settings=auth_settings,
                                        async=params.get('async'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def sign_ex(self, body, async=False, **kwargs):
        """
        Sign data with a private key. The signing key must be an asymmetric key with the private part present. The sign operation must be enabled for this key. Symmetric keys  may not be used to sign data. They can be used with the computeMac and verifyMac methods. <br> The data must be hashed with a SHA-1 or SHA-2 family hash algorithm. 
        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{SignRequestEx}
        @param body: Signature request (required)
        @rtype: L{SignResponse}
        @return:
        
        If the method is called asynchronously, returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if async:
            return self.sign_ex_with_http_info(body, async=async, **kwargs)
        else:
            (data) = self.sign_ex_with_http_info(body, async=async, **kwargs)
            return data

    def sign_ex_with_http_info(self, body, async=False, **kwargs):
        """
        Sign data with a private key. The signing key must be an asymmetric key with the private part present. The sign operation must be enabled for this key. Symmetric keys  may not be used to sign data. They can be used with the computeMac and verifyMac methods. <br> The data must be hashed with a SHA-1 or SHA-2 family hash algorithm. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True::
            >>> thread = api.sign_ex_with_http_info(body, async=True)
            >>> result = thread.get()

        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{SignRequestEx}
        @param body: Signature request (required)
        @rtype: L{SignResponse}
        @return:

        If the method is called asynchronously, returns the request thread.
        """

        all_params = ['body']
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sign_ex" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `sign_ex`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['bearerToken']

        return self.api_client.call_api('/crypto/v1/sign', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='SignResponse',
                                        auth_settings=auth_settings,
                                        async=params.get('async'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def verify(self, key_id, body, async=False, **kwargs):
        """
        Verify a signature with a public key. The verifying key must be an asymmetric key with the verify operation enabled. Symmetric keys may not be used to verify data. They can be used with the computeMac and verifyMac operations. <br> The signature must have been created with a SHA-1 or SHA-2 family hash algorithm. 
        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type key_id: L{str}
        @param key_id: kid of security object (required)
        @type body: L{VerifyRequest}
        @param body: Verification request (required)
        @rtype: L{VerifyResponse}
        @return:
        
        If the method is called asynchronously, returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if async:
            return self.verify_with_http_info(key_id, body, async=async, **kwargs)
        else:
            (data) = self.verify_with_http_info(key_id, body, async=async, **kwargs)
            return data

    def verify_with_http_info(self, key_id, body, async=False, **kwargs):
        """
        Verify a signature with a public key. The verifying key must be an asymmetric key with the verify operation enabled. Symmetric keys may not be used to verify data. They can be used with the computeMac and verifyMac operations. <br> The signature must have been created with a SHA-1 or SHA-2 family hash algorithm. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True::
            >>> thread = api.verify_with_http_info(key_id, body, async=True)
            >>> result = thread.get()

        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type key_id: L{str}
        @param key_id: kid of security object (required)
        @type body: L{VerifyRequest}
        @param body: Verification request (required)
        @rtype: L{VerifyResponse}
        @return:

        If the method is called asynchronously, returns the request thread.
        """

        all_params = ['key_id', 'body']
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method verify" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'key_id' is set
        if ('key_id' not in params) or (params['key_id'] is None):
            raise ValueError("Missing the required parameter `key_id` when calling `verify`")
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `verify`")


        collection_formats = {}

        path_params = {}
        if 'key_id' in params:
            path_params['key-id'] = params['key_id']

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['bearerToken']

        return self.api_client.call_api('/crypto/v1/keys/{key-id}/verify', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='VerifyResponse',
                                        auth_settings=auth_settings,
                                        async=params.get('async'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)

    def verify_ex(self, body, async=False, **kwargs):
        """
        Verify a signature with a public key. The verifying key must be an asymmetric key with the verify operation enabled. Symmetric keys may not be used to verify data. They can be used with the computeMac and verifyMac operations. <br> The signature must have been created with a SHA-1 or SHA-2 family hash algorithm. 
        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{VerifyRequestEx}
        @param body: Verification request (required)
        @rtype: L{VerifyResponse}
        @return:
        
        If the method is called asynchronously, returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if async:
            return self.verify_ex_with_http_info(body, async=async, **kwargs)
        else:
            (data) = self.verify_ex_with_http_info(body, async=async, **kwargs)
            return data

    def verify_ex_with_http_info(self, body, async=False, **kwargs):
        """
        Verify a signature with a public key. The verifying key must be an asymmetric key with the verify operation enabled. Symmetric keys may not be used to verify data. They can be used with the computeMac and verifyMac operations. <br> The signature must have been created with a SHA-1 or SHA-2 family hash algorithm. 
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True::
            >>> thread = api.verify_ex_with_http_info(body, async=True)
            >>> result = thread.get()

        @type async: bool
        @param async: Whether the call should be performed asynchronously. (Default is False).
        @type body: L{VerifyRequestEx}
        @param body: Verification request (required)
        @rtype: L{VerifyResponse}
        @return:

        If the method is called asynchronously, returns the request thread.
        """

        all_params = ['body']
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method verify_ex" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `verify_ex`")


        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])

        # Authentication setting
        auth_settings = ['bearerToken']

        return self.api_client.call_api('/crypto/v1/verify', 'POST',
                                        path_params,
                                        query_params,
                                        header_params,
                                        body=body_params,
                                        post_params=form_params,
                                        files=local_var_files,
                                        response_type='VerifyResponse',
                                        auth_settings=auth_settings,
                                        async=params.get('async'),
                                        _return_http_data_only=params.get('_return_http_data_only'),
                                        _preload_content=params.get('_preload_content', True),
                                        _request_timeout=params.get('_request_timeout'),
                                        collection_formats=collection_formats)
