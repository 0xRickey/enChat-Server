import json
from libs.Decryptor import Decryptor
from libs.Requests.Request import Request

class RequestFactory:
    def __init__(self, decryptor: Decryptor):
        self.decryptor = decryptor

    def extract_request(self, encrypted_request: bytes):
        decrypted_request = self.decryptor.decrypt_message(encrypted_request)
        request_dict: dict = json.loads(decrypted_request.decode())
        
        return Request(request_dict)