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
class EncryptRequest(object):
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
        'alg': 'ObjectType',
        'plain': 'bytearray',
        'mode': 'CryptMode',
        'iv': 'bytearray',
        'ad': 'bytearray',
        'tag_len': 'int'
    }

    attribute_map = {
        'alg': 'alg',
        'plain': 'plain',
        'mode': 'mode',
        'iv': 'iv',
        'ad': 'ad',
        'tag_len': 'tag_len'
    }

    def __init__(self, alg=None, plain=None, mode=None, iv=None, ad=None, tag_len=None):
        """
        EncryptRequest - a model defined in Swagger
        """

        self._alg = None
        self._plain = None
        self._mode = None
        self._iv = None
        self._ad = None
        self._tag_len = None

        self.alg = alg
        self.plain = plain
        if mode is not None:
          self.mode = mode
        if iv is not None:
          self.iv = iv
        if ad is not None:
          self.ad = ad
        if tag_len is not None:
          self.tag_len = tag_len

    @property
    def alg(self):
        """
        Gets the alg of this EncryptRequest.

        Type: L{ObjectType}
        """
        return self._alg

    @alg.setter
    def alg(self, alg):
        """
        Sets the alg of this EncryptRequest.
        """

        self._alg = alg

    @property
    def plain(self):
        """
        Gets the plain of this EncryptRequest.
        The plaintext to encrypt.

        Type: L{bytearray}
        """
        return self._plain

    @plain.setter
    def plain(self, plain):
        """
        Sets the plain of this EncryptRequest.
        The plaintext to encrypt.
        """

        if not isinstance(plain, bytearray):
            raise ValueError("Invalid value for `plain`, `plain` must be a bytearray")
        self._plain = plain

    @property
    def mode(self):
        """
        Gets the mode of this EncryptRequest.

        Type: L{CryptMode}
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """
        Sets the mode of this EncryptRequest.
        """

        self._mode = mode

    @property
    def iv(self):
        """
        Gets the iv of this EncryptRequest.
        For symmetric ciphers, this value will be used for the cipher initialization value. If not provided, SDKMS will generate a random iv and return it in the response. If provided, iv length must match the length required by the cipher and mode. 

        Type: L{bytearray}
        """
        return self._iv

    @iv.setter
    def iv(self, iv):
        """
        Sets the iv of this EncryptRequest.
        For symmetric ciphers, this value will be used for the cipher initialization value. If not provided, SDKMS will generate a random iv and return it in the response. If provided, iv length must match the length required by the cipher and mode. 
        """

        if not isinstance(iv, bytearray):
            raise ValueError("Invalid value for `iv`, `iv` must be a bytearray")
        self._iv = iv

    @property
    def ad(self):
        """
        Gets the ad of this EncryptRequest.
        For symmetric ciphers with cipher mode GCM or CCM, this optionally specifies the authenticated data used by the cipher. This field must not be provided with other cipher modes. 

        Type: L{bytearray}
        """
        return self._ad

    @ad.setter
    def ad(self, ad):
        """
        Sets the ad of this EncryptRequest.
        For symmetric ciphers with cipher mode GCM or CCM, this optionally specifies the authenticated data used by the cipher. This field must not be provided with other cipher modes. 
        """

        if not isinstance(ad, bytearray):
            raise ValueError("Invalid value for `ad`, `ad` must be a bytearray")
        self._ad = ad

    @property
    def tag_len(self):
        """
        Gets the tag_len of this EncryptRequest.
        For symmetric ciphers with cipher mode GCM or CCM, this field specifies the length of the authentication tag to be produced. This field is specified in bits (not bytes). This field is required for symmetric ciphers with cipher mode GCM or CCM. It must not be specified for asymmetric ciphers and symmetric ciphers with other cipher modes.

        Type: L{int}
        """
        return self._tag_len

    @tag_len.setter
    def tag_len(self, tag_len):
        """
        Sets the tag_len of this EncryptRequest.
        For symmetric ciphers with cipher mode GCM or CCM, this field specifies the length of the authentication tag to be produced. This field is specified in bits (not bytes). This field is required for symmetric ciphers with cipher mode GCM or CCM. It must not be specified for asymmetric ciphers and symmetric ciphers with other cipher modes.
        """

        self._tag_len = tag_len

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
        if not isinstance(other, EncryptRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

