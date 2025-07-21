import json
from libs.KeyManager import KeyManager
from hashlib import sha256
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class Request:
    def __init__(self, request_dict: dict):
        self.message = request_dict["MESSAGE"]
        self.signature = request_dict["SIGNATURE"]

    def verify_integrity(self) -> bool:
        # Turn the message into a JSON string and then bytes
        msg_hash = sha256(json.dumps(self.message).encode()).digest()

        # Verify the signature by using the public key and hash
        signer_pub_key = serialization.load_pem_public_key(
            self.get_metadata()["PUBLIC_KEY"].encode()
        )

        try:
            signer_pub_key.verify(
                self.signature,
                msg_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Error verifying integrity: {e}")
            return False

    def get_command(self):
        return self.message["COMMAND"]
    
    def get_payload(self):
        return self.message["PAYLOAD"]
    
    def get_metadata(self):
        return self.message["METADATA"]
    
    def get_signature(self):
        return self.signature