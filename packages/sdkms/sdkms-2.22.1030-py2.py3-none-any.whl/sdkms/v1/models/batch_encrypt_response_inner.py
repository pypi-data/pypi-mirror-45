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
class BatchEncryptResponseInner(object):
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
        'status': 'int',
        'error': 'str',
        'body': 'EncryptResponse'
    }

    attribute_map = {
        'status': 'status',
        'error': 'error',
        'body': 'body'
    }

    def __init__(self, status=None, error=None, body=None):
        """
        BatchEncryptResponseInner - a model defined in Swagger
        """

        self._status = None
        self._error = None
        self._body = None

        self.status = status
        if error is not None:
          self.error = error
        if body is not None:
          self.body = body

    @property
    def status(self):
        """
        Gets the status of this BatchEncryptResponseInner.
        The HTTP status code for this partial request.

        Type: L{int}
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this BatchEncryptResponseInner.
        The HTTP status code for this partial request.
        """

        self._status = status

    @property
    def error(self):
        """
        Gets the error of this BatchEncryptResponseInner.
        When the status property indicates an error, this contains the error message.

        Type: L{str}
        """
        return self._error

    @error.setter
    def error(self, error):
        """
        Sets the error of this BatchEncryptResponseInner.
        When the status property indicates an error, this contains the error message.
        """

        self._error = error

    @property
    def body(self):
        """
        Gets the body of this BatchEncryptResponseInner.

        Type: L{EncryptResponse}
        """
        return self._body

    @body.setter
    def body(self, body):
        """
        Sets the body of this BatchEncryptResponseInner.
        """

        self._body = body

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
        if not isinstance(other, BatchEncryptResponseInner):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

