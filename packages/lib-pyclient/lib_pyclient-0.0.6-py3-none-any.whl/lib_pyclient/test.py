import http.client

#import lib_pyclient.pywebapi
from lib_pyclient.pywebapi import ObjectMethodResult, HttpApiResult, RequestParams, http_request, print_full_response
from lib_pyclient.pywebapibase import ApiBase
from lib_pyclient.pyconvert import object_to_dict


""" Models """
class BmTest(object):
    def __init__(self, firstname, lastname, *args, **kwargs):
        self.firstname = firstname
        self.lastname = lastname


class ApiController1(ApiBase):

    """ http_s_con may be HTTPConnection or HTTPSConnection """
    def __init__(self, http_s_con, lang_code_ui="en-US"):
        super().__init__(http_s_con,lang_code_ui)
        self.controller = "/api/Controller1/" 

    def api_1(self, bm, lang_code_data) -> HttpApiResult:
        api_name = "ApiName1"
        headers = {}
        headers.update({'Authorization': "Bearer " + self.access_token})
        headers.update({'Accept': "application/json"})
        headers.update({'Content-Type': "application/json"}) # application/x-www-form-urlencoded
        headers.update({'LANG-CODE-UI': self.lang_code_ui})
        headers.update({'LANG-CODE-DATA': lang_code_data})

        #body = {}
        #body.update(object_to_dict(bm_secured_package))
        body = object_to_dict(bm)

        request_params = RequestParams(host=self.host,
                                       request_type="POST",
                                       api=self.controller + api_name,
                                       headers=headers,
                                       body=body)

        response = http_request(request_params, self.http_connection)



        return response



host = "localhost:5000"
default_lang_code_data = "en-US"
default_lang_code_ui = "en-US"
http_s_connection = http.client.HTTPConnection(host)
#http_s_connection = http.client.HTTPSConnection(host)

bm = BmTest("John","Brown")
my_api = ApiController1(http_s_connection)

response = my_api.api_1(bm, default_lang_code_data)
print_full_response(response)

#if (response.object_method_result.isSuccess):
#    response_secure_comm_package = BmSecureCommPackage(**response.object_method_result.obj)
#else:
#    response_secure_comm_package = None


