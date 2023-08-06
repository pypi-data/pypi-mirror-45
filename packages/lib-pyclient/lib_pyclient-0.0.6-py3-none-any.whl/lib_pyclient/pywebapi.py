# Method 1 (without path/package )
"""
import os, sys
try:
    import objectmethodresult
except:
    # using relative import
    from . import objectmethodresult
    # discover path of the module and add it to the sys.path.
    path = os.path.dirname(objectmethodresult.__file__)
    sys.path.insert(0, path)
    #print("adding path",path)

from objectmethodresult import ObjectMethodResult,MessageResult, ExceptionMessage,EnumMsgType
"""
# Method 2 (with package/path name)
"""
from lib_pyclient.objectmethodresult import ObjectMethodResult,MessageResult, ExceptionMessage,EnumMsgType
"""

import json
import copy
import ctypes
from lib_pyclient.objectmethodresult import ObjectMethodResult,MessageResult, ExceptionMessage,EnumMsgType
from lib_pyclient.pyconvert import toUnSigned32

class HttpApiResult():
    def __init__(self):
        self.is_success = False
        self.response_headers = "";
        self.response_status_code=0;
        self.response_reason = "";
        self.response_json = {} # -> to be converted to ObjectMethodResult
        self.response_raw = bytes() #""

        # Boş bir ObjectMetyhodResult yaratıyoruz, bunu yapmazsak intellisense çalışmıyor
        self.object_method_result = ObjectMethodResult(False, None,(),"")


class RequestParams():
    def __init__(self,host=None,request_type="GET",api="",headers=None,body=None):
        self.host = host
        self.request_type=request_type
        self.api=api
        self.headers=headers
        self.body=body


def print_full_response(response:HttpApiResult):
    print("api result:", response.is_success)
    print("object method result:", response.object_method_result.isSuccess)
    print("object method err msg:", response.object_method_result.errMsg)

    messages = response.object_method_result.messages
    msg_count = len(messages)
    print("object method message count:", msg_count)
    for i in range(msg_count):
        message = messages[i]
        print(f"Message:{str(i)}, {EnumMsgType(message.msgType).name}, {message.msg}, Code:{message.msgCode}, Sender:{message.sender}, DateTime:{message.dateTime}")
        for x in range(len(message.exceptionList)):
            exception_message = message.exceptionList[x]
            unsigned_exception_code = toUnSigned32(exception_message.exception_code) #exception_message.exception_code & 0xffffffff
            unsigned_exception_code_hex = hex(unsigned_exception_code)
            print(f" - Exception:{str(x)} , {exception_message.exception_msg}, Code:{exception_message.exception_code}({unsigned_exception_code_hex})")


    print("status code:", response.response_status_code)
    print("reason:", response.response_reason)
    print("headers:", response.response_headers)
    print("raw:", response.response_raw)
    print("json:", response.response_json)

#def http_request(request_type: "GET", api_host: "localhost:5000", api="/api/Product/1", headers=None, body=None):
def http_request(request_params:RequestParams,http_connection, is_object_method_result=True) -> HttpApiResult:

    result = HttpApiResult()
    try:
        print('['+request_params.request_type+']',request_params.host+request_params.api)
        print(" Header:",request_params.headers)
        print(" Body:",request_params.body)

        #http_connection = http.client.HTTPConnection(request_params.host)
        http_connection.request(request_params.request_type,request_params.api, body=json.dumps(request_params.body), headers=request_params.headers)
        response = http_connection.getresponse()
        result.response_reason = response.reason
        result.response_headers = response.headers
        result.response_status_code = response.status
        result.response_raw = response.read()
        if len(result.response_raw)>0:
            #result.object_method_result = json.load(result.response_raw.decode())
            #print("result.object_method_result",result.object_method_result)
            result.response_json = json.loads(result.response_raw.decode())

            if (is_object_method_result):
                object_method_result = ObjectMethodResult(**result.response_json)
                result.object_method_result = object_method_result

        if (response.status == 200) or (response.status == 201):
            result.is_success = True
        else:
            # Sucess
            result.is_success = False
    except: #(RuntimeError, TypeError, NameError):
        print('Exception occured',sys.exc_info()[0],sys.exc_info()[1])
    finally:
        #http_connection.close()
        return result
