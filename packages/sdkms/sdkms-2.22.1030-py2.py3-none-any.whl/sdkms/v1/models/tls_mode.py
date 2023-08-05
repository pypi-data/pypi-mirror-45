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

from .base_enum_object import BaseEnumObject

# NOTE: This class is auto generated by the swagger code generator program.
# Do not edit the class manually.
class TlsMode(BaseEnumObject):
    """
    TLS mod.

    Enumeration values::
        TlsMode.DISABLED = "disabled"
        TlsMode.OPPORTUNISTIC = "opportunistic"
        TlsMode.REQUIRED = "required"

    This class doesnt use python standard enumeration since they dont support unknown values. 
    
    This is an object of type BaseEnumObject and provides similar functionality as a String Enumeration.
    
    Get a standard instance of enum: TlsMode.FOO or TlsMode("FOO")
    Get non standard instance of enum: TlsMode("BAR")
    Enum instance to String value: TlsMode.FOO.value , TlsMode.FOO.name (Gives "FOO")
    Equality: TlsMode.FOO == TlsMode("FOO") , TlsMode.FOO != TlsMode.BAR
    Provides str func:  str(TlsMode.FOO) == "TlsMode.FOO"
    
    Also the class maintains a static dict of values. hence TlsMode.FOO and TlsMode("FOO") are really backed by same data. 
    """
    
    """
    Inner class that stores the actual value
    """
    class __TlsMode(BaseEnumObject):

        def __init__(self, value):
            self.__value = value

        @property
        def value(self):
            return self.__value

        @property
        def name(self):
            return self.__value

        def __str__(self):
            return "TlsMode." + self.__value

    """
    allowed enum values
    """
    DISABLED = __TlsMode("disabled")
    OPPORTUNISTIC = __TlsMode("opportunistic")
    REQUIRED = __TlsMode("required")

    """
    dictionary that keeps the enum value mapping for static access
    """
    __VALUES = dict()
    __VALUES["disabled"] = DISABLED
    __VALUES["opportunistic"] = OPPORTUNISTIC
    __VALUES["required"] = REQUIRED

    def __init__(self, name):
        if name in TlsMode.__VALUES:
            self.__instance = TlsMode.__VALUES[name]
        else:
            new_value = TlsMode.__TlsMode(name)
            TlsMode.__VALUES[name] = new_value
            self.__instance = new_value

    @property
    def value(self):
        return self.__instance.value

    @property
    def name(self):
        return self.__instance.name

    def __str__(self):
        return "TlsMode." + self.__instance.name

    """ 
    This is to ensure equals work for both static defined values and client defined ones.
    """
    def __eq__(self, other):
        if (isinstance(self, TlsMode) or isinstance(self, TlsMode.__TlsMode)) and \
                (isinstance(other, TlsMode) or isinstance(other, TlsMode.__TlsMode)):
                return self.value == other.value

        return False

    def __ne__(self, other):
        if (isinstance(self, TlsMode) or isinstance(self, TlsMode.__TlsMode)) and \
                (isinstance(other, TlsMode) or isinstance(other, TlsMode.__TlsMode)):
                return self.value != other.value

        return True


