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
class DecryptRequest(object):
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
        'cipher': 'bytearray',
        'mode': 'CryptMode',
        'iv': 'bytearray',
        'ad': 'bytearray',
        'tag': 'bytearray'
    }

    attribute_map = {
        'alg': 'alg',
        'cipher': 'cipher',
        'mode': 'mode',
        'iv': 'iv',
        'ad': 'ad',
        'tag': 'tag'
    }

    def __init__(self, alg=None, cipher=None, mode=None, iv=None, ad=None, tag=None):
        """
        DecryptRequest - a model defined in Swagger
        """

        self._alg = None
        self._cipher = None
        self._mode = None
        self._iv = None
        self._ad = None
        self._tag = None

        if alg is not None:
          self.alg = alg
        self.cipher = cipher
        if mode is not None:
          self.mode = mode
        if iv is not None:
          self.iv = iv
        if ad is not None:
          self.ad = ad
        if tag is not None:
          self.tag = tag

    @property
    def alg(self):
        """
        Gets the alg of this DecryptRequest.

        Type: L{ObjectType}
        """
        return self._alg

    @alg.setter
    def alg(self, alg):
        """
        Sets the alg of this DecryptRequest.
        """

        self._alg = alg

    @property
    def cipher(self):
        """
        Gets the cipher of this DecryptRequest.
        The ciphertext to decrypt.

        Type: L{bytearray}
        """
        return self._cipher

    @cipher.setter
    def cipher(self, cipher):
        """
        Sets the cipher of this DecryptRequest.
        The ciphertext to decrypt.
        """

        if not isinstance(cipher, bytearray):
            raise ValueError("Invalid value for `cipher`, `cipher` must be a bytearray")
        self._cipher = cipher

    @property
    def mode(self):
        """
        Gets the mode of this DecryptRequest.

        Type: L{CryptMode}
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """
        Sets the mode of this DecryptRequest.
        """

        self._mode = mode

    @property
    def iv(self):
        """
        Gets the iv of this DecryptRequest.
        The initialization value used to encrypt this ciphertext. This field is required for symmetric ciphers, and ignored for asymmetric ciphers. 

        Type: L{bytearray}
        """
        return self._iv

    @iv.setter
    def iv(self, iv):
        """
        Sets the iv of this DecryptRequest.
        The initialization value used to encrypt this ciphertext. This field is required for symmetric ciphers, and ignored for asymmetric ciphers. 
        """

        if not isinstance(iv, bytearray):
            raise ValueError("Invalid value for `iv`, `iv` must be a bytearray")
        self._iv = iv

    @property
    def ad(self):
        """
        Gets the ad of this DecryptRequest.
        The authenticated data used with this ciphertext and authentication tag. This field is required for symmetric ciphers using cipher mode GCM or CCM, and must not be specified for all other ciphers. 

        Type: L{bytearray}
        """
        return self._ad

    @ad.setter
    def ad(self, ad):
        """
        Sets the ad of this DecryptRequest.
        The authenticated data used with this ciphertext and authentication tag. This field is required for symmetric ciphers using cipher mode GCM or CCM, and must not be specified for all other ciphers. 
        """

        if not isinstance(ad, bytearray):
            raise ValueError("Invalid value for `ad`, `ad` must be a bytearray")
        self._ad = ad

    @property
    def tag(self):
        """
        Gets the tag of this DecryptRequest.
        The authentication tag used with this ciphertext and authenticated data. This field is required for symmetric ciphers using cipher mode GCM or CCM, and must not be specified for all other ciphers. 

        Type: L{bytearray}
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """
        Sets the tag of this DecryptRequest.
        The authentication tag used with this ciphertext and authenticated data. This field is required for symmetric ciphers using cipher mode GCM or CCM, and must not be specified for all other ciphers. 
        """

        if not isinstance(tag, bytearray):
            raise ValueError("Invalid value for `tag`, `tag` must be a bytearray")
        self._tag = tag

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
        if not isinstance(other, DecryptRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

