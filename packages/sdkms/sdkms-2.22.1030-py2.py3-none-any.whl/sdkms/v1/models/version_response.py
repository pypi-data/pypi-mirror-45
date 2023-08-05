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


from pprint import pformat
from six import iteritems
import re




# NOTE: This class is auto generated by the swagger code generator program.
# Do not edit the class manually.
class VersionResponse(object):
    """
    @undocumented: swagger_types
    @undocumented: attribute_map
    @undocumented: to_dict
    @undocumented: to_str
    @undocumented: __repr__
    @undocumented: __eq__
    @undocumented: __ne__
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'version': 'str',
        'api_version': 'str',
        'server_mode': 'ServerMode',
        'fips_level': 'int'
    }

    attribute_map = {
        'version': 'version',
        'api_version': 'api_version',
        'server_mode': 'server_mode',
        'fips_level': 'fips_level'
    }

    def __init__(self, version=None, api_version=None, server_mode=None, fips_level=None):
        """
        VersionResponse - a model defined in Swagger
        """

        self._version = None
        self._api_version = None
        self._server_mode = None
        self._fips_level = None

        self.version = version
        self.api_version = api_version
        self.server_mode = server_mode
        if fips_level is not None:
          self.fips_level = fips_level

    @property
    def version(self):
        """
        Gets the version of this VersionResponse.
        The SDKMS server version. This is encoded as major.minor.build. For example, 1.0.25. 

        Type: L{str}
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this VersionResponse.
        The SDKMS server version. This is encoded as major.minor.build. For example, 1.0.25. 
        """

        self._version = version

    @property
    def api_version(self):
        """
        Gets the api_version of this VersionResponse.
        The API version implemented by this server.

        Type: L{str}
        """
        return self._api_version

    @api_version.setter
    def api_version(self, api_version):
        """
        Sets the api_version of this VersionResponse.
        The API version implemented by this server.
        """

        self._api_version = api_version

    @property
    def server_mode(self):
        """
        Gets the server_mode of this VersionResponse.

        Type: L{ServerMode}
        """
        return self._server_mode

    @server_mode.setter
    def server_mode(self, server_mode):
        """
        Sets the server_mode of this VersionResponse.
        """

        self._server_mode = server_mode

    @property
    def fips_level(self):
        """
        Gets the fips_level of this VersionResponse.
        FIPS level at which SDKMS in running. If this field is absent, then SDKMS is not running in FIPS compliant mode.

        Type: L{int}
        """
        return self._fips_level

    @fips_level.setter
    def fips_level(self, fips_level):
        """
        Sets the fips_level of this VersionResponse.
        FIPS level at which SDKMS in running. If this field is absent, then SDKMS is not running in FIPS compliant mode.
        """

        self._fips_level = fips_level

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, VersionResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

