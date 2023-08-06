from abc import ABC, abstractmethod





class ApiBase(ABC):
    #def __del__(self):
        # If command is destroyed or created new we should release dll resources before new command is created.
        # It is recommended to create only one instance of command.

    def __init__(self, http_s_con, lang_code_ui):
        if (lang_code_ui==""):
            lang_code_ui = "en-US"

        self.access_token = ""
        self.host = http_s_con.host + ":" + str(http_s_con.port)
        self.lang_code_ui = lang_code_ui
        self.http_connection = http_s_con
        # self.http_connection =  http.client.HTTPConnection(host)  # "localhost:5000")
        print("lang_code_ui",lang_code_ui)
    #@abstractmethod (cant be abstract because every command may have different command parameters)
    #def build(self, nodeAddress=0):
    #    pass

    #@abstractmethod
    #def get_response(self):
    #    pass
