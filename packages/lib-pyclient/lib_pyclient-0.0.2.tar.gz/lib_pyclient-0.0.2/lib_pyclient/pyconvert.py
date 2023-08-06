import json
import inspect
from typing import Generic

class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj


# Her iki yöntem de aynı sonucu verir, OnjectEncoder'lı verisyonu nested objeleri de iceriyormus.
def toJSON(obj, sort_keys=False, indent=4):
    return json.dumps(obj,cls=ObjectEncoder, sort_keys=sort_keys, indent=indent)
    # Test edilmedi ->
    #return json.dumps(obj,cls=json.JSONEncoder, sort_keys=sort_keys, indent=indent)

#def toJSON(obj, sort_keys=False, indent=4):
#    return json.dumps(obj, default=lambda o: o.__dict__,sort_keys=sort_keys, indent=indent)

def dict_get(obj):
    # Basic->
    return obj.__dict__

def object_to_dict(obj):
    # dictionary is sorted
    # Complex, create new ->
    d = dict(
        (key, value)
        for key, value in inspect.getmembers(obj)
        if not key.startswith("__")
        and not inspect.isabstract(value)
        and not inspect.isbuiltin(value)
        and not inspect.isfunction(value)
        and not inspect.isgenerator(value)
        and not inspect.isgeneratorfunction(value)
        and not inspect.ismethod(value)
        and not inspect.ismethoddescriptor(value)
        and not inspect.isroutine(value)
    )
    return d

"""
kod içerisinde direkt çağırırsak, e'nin field ları intellisensede geliyor.
dict_to_object dersek obje yine oluşuyor fakat intellisense kullanmıyoruz
e = ExceptionMessage(**exception_message1)
"""
def dict_to_object(cls, data:dict):
    return cls(**data)



def toHEX(obj, prefix="0x", space_string=" "):
    res =""
    for i in range(len(obj)):
        res += prefix +"{:02x}".format(obj[i]) + space_string
    return res

def printHEX(obj, prefix="0x", space_string=" "):
    for i in range(len(obj)):
        print(prefix + "{:02x}".format(obj[i]), end=space_string)
    print("")


# print(format(obj[i],"02x"),end=space_string)


def toUnSigned32(n):
    n = n & 0xffffffff
    return n

#def toSigned32(n):
#    n = n & 0xffffffff
#    return n | (-(n & 0x80000000))

def toSigned32(n):
    n = n & 0xffffffff
    return (n ^ 0x80000000) - 0x80000000