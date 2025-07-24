import json
from libs.response.Response import Response

class AesEncryptedResponse:
    def __init__(self, ciphertext: bytes, signature: bytes, init_vec: bytes):
        self.ciphertext = ciphertext
        self.signature  = signature
        self.init_vec   = init_vec

    def as_bytes(self) -> bytes:
        return self.as_json_str().encode()

    def as_json_str(self) -> str:
        return json.loads(self.as_dict()) 

    def as_dict(self) -> dict:
        return {
            "CIPHERTEXT": self.ciphertext.decode(),
            "SIGNATURE": self.signature.decode(),
            "PUBLIC_KEY": "",
            "IV": self.init_vec.decode()
        }