from enum import IntEnum
from typing import List


class EnumMsgType(IntEnum):
    ERROR = 0,
    SUCCESS = 1,
    INFO = 2,
    WARNING = 3,
    LOG = 4



class ExceptionMessage(object):


    def __init__(self, exception_msg, exception_code:int, *args, **kwargs):
        self.exception_msg = exception_msg
        self.exception_code = exception_code

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(**json_data)

class MessageResult(object):
    def __init__(self,isSuccess, msg, msgType:EnumMsgType, msgCode, sender, dateTime, exceptionList:List[ExceptionMessage],*args, **kwargs):
        self.isSuccess = isSuccess
        self.msg = msg
        self.msgType = msgType
        self.msgCode = msgCode
        self.sender = sender
        self.dateTime = dateTime

        print(type(exceptionList))
        mp = map(ExceptionMessage.from_json,exceptionList)  #data["exceptionList"])
        ls = list(mp)
        self.exceptionList = ls

        #for i in range(len(data['exceptionList'])):
        #    self.exceptionList.append(data['exceptionList'][i])

    @classmethod
    def from_json(cls, json_data: dict):
        return cls(**json_data)


class ObjectMethodResult(object):
    def __init__(self,isSuccess, obj, messages:List[MessageResult], errMsg ):
        self.isSuccess = isSuccess
        self.obj = obj
        self.errMsg = errMsg
        mp = map(MessageResult.from_json,messages)
        ls = list(mp)
        self.messages = ls


    @classmethod
    def from_json(cls, json_data: dict):
        return cls(**json_data)


"""
exception_message_list = list()
exception_message1 = dict(exception_msg='Excepiton Message 1', exception_code='1')
exception_message2 = dict(exception_msg='Excepiton Message 2', exception_code='2')
exception_message_list.append(exception_message1)
exception_message_list.append(exception_message2)
message_result = dict(exceptionList=exception_message_list, msg='Message1', msgType=0, msgCode=0, isSuccess=0, sender='', dateTime='')

message_result_list = list()
message_result_list.append(message_result)
object_method_result = dict(isSuccess=False, obj="my string obj", messages=message_result_list,errMsg="test err msg")

#jdump = json.dumps(message_result)
jdump = json.dumps(object_method_result, indent=2)
print(jdump)
"""