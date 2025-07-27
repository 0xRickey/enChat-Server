import json, uuid

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.primitives import serialization

class Response:
    def __init__(
        self,
        status: str,
        payload: dict,
        metadata: dict,
        signature: str,
        pubKey: RSAPublicKey,
        init_vec: bytes = None
    ):
        # encrypted and included in the reply to client
        self.status = status
        self.payload = payload
        self.metadata = metadata

        # unencrypted and included in the reply to client
        self.signature: str = signature
        self.pubKey: RSAPublicKey = pubKey
        self.init_vec: bytes = init_vec

        # serverside logging, not included in reply to client
        self.response_id = str(uuid.uuid4())

    def get_status(self):
        return self.status

    def get_payload(self):
        return self.payload

    def get_metadata(self):
        return self.metadata

    def get_response_id(self):
        return self.response_id
    
    def get_init_vec(self) -> bytes:
        return self.init_vec

    def set_init_vec(self, init_vec: bytes):
        self.init_vec = init_vec

    def get_pub_key(self) -> RSAPublicKey:
        return self.pubKey

    def get_PEM_pub_key(self):
        return self.pubKey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

    def set_pub_key(self, pubKey: RSAPublicKey):
        self.pubKey = pubKey
    
    def get_signature(self):
        return self.signature
    
    def get_message(self):
        return {
            "STATUS": self.status,
            "PAYLOAD": self.payload,
            "METADATA": self.metadata
        }

    def as_dict(self):
        return {
            "MESSAGE": self.get_message(),
            "SIGNATURE": self.signature,
            "PUBLIC_KEY": self.get_PEM_pub_key(),
            "IV": self.init_vec
        }

    def as_bytes(self):
        return json.dumps(self.as_dict()).encode()