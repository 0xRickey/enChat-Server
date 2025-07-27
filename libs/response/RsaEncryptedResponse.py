import json, base64

class RsaEncryptedResponse():
    def __init__(
        self,
        ciphertext: bytes,
        signature: str,
        pubKey: str,
    ) -> None:
        self.ciphertext = ciphertext
        self.signature = signature
        self.pubKey = pubKey

    def as_dict(self):
        return {
            "CIPHERTEXT": base64.b64encode(self.ciphertext).decode('utf-8'),
            "SIGNATURE": self.signature,
            "PUBLIC_KEY": self.pubKey,
            "IV": ""
        }
    
    def as_bytes(self):
        return json.dumps(self.as_dict()).encode()