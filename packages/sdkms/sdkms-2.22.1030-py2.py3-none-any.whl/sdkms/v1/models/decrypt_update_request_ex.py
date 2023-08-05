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
class DecryptUpdateRequestEx(object):
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
        'key': 'SobjectDescriptor',
        'cipher': 'bytearray',
        'state': 'bytearray'
    }

    attribute_map = {
        'key': 'key',
        'cipher': 'cipher',
        'state': 'state'
    }

    def __init__(self, key=None, cipher=None, state=None):
        """
        DecryptUpdateRequestEx - a model defined in Swagger
        """

        self._key = None
        self._cipher = None
        self._state = None

        self.key = key
        self.cipher = cipher
        self.state = state

    @property
    def key(self):
        """
        Gets the key of this DecryptUpdateRequestEx.

        Type: L{SobjectDescriptor}
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this DecryptUpdateRequestEx.
        """

        self._key = key

    @property
    def cipher(self):
        """
        Gets the cipher of this DecryptUpdateRequestEx.
        Ciphertext to decrypt.

        Type: L{bytearray}
        """
        return self._cipher

    @cipher.setter
    def cipher(self, cipher):
        """
        Sets the cipher of this DecryptUpdateRequestEx.
        Ciphertext to decrypt.
        """

        if not isinstance(cipher, bytearray):
            raise ValueError("Invalid value for `cipher`, `cipher` must be a bytearray")
        self._cipher = cipher

    @property
    def state(self):
        """
        Gets the state of this DecryptUpdateRequestEx.

        Type: L{bytearray}
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this DecryptUpdateRequestEx.
        """

        if not isinstance(state, bytearray):
            raise ValueError("Invalid value for `state`, `state` must be a bytearray")
        self._state = state

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
        if not isinstance(other, DecryptUpdateRequestEx):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

