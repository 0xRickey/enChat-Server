from libs.response.Response import Response

class ResponseLog:
    def __init__(self):
        self.response_log = {}

    def add_response(self, response: Response):
        self.response_log[response.get_response_id()] = response

    def get_response(self, response_id: str):
        return self.response_log[response_id]