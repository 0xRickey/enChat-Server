import json, base64

class AesEncryptedResponse:
    def __init__(self, ciphertext: bytes, signature: bytes, init_vec: bytes):
        self.ciphertext = ciphertext
        self.signature  = signature
        self.init_vec   = init_vec

    def as_bytes(self) -> bytes:
        return self.as_json_str().encode()

    def as_json_str(self) -> str:
        return json.dumps(self.as_dict()) 

    def as_dict(self) -> dict:
        return {
            "CIPHERTEXT": base64.b64encode(self.ciphertext).decode('utf-8'),
            "SIGNATURE": self.signature.decode(),
            "PUBLIC_KEY": "",
            "IV": base64.b64encode(self.init_vec).decode('utf-8')
        }