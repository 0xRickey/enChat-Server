import json
from libs.KeyManager import KeyManager
from hashlib import sha256
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

class Request:
    def __init__(
        self,
        command: str,
        payload: dict,
        metadata: dict,
        signature: str,
        pubKey: str,
        init_vec: str
    ):
        self.command = command
        self.payload = payload
        self.metadata = metadata
        self.signature = signature
        self.pubKey = pubKey
        self.init_vec = init_vec

    def verify_integrity(self) -> bool:
        # Turn the message into a JSON string and then bytes
        msg_hash = sha256(json.dumps(self.get_message()).encode()).hexdigest()

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
        
    def get_message(self) -> dict:
        return {
            "COMMAND": self.command,
            "PAYLOAD": self.payload,
            "METADATA": self.metadata
        }

    def get_command(self) -> str:
        return self.command
    
    def get_payload(self) -> dict:
        return self.payload
    
    def get_metadata(self) -> dict:
        return self.metadata
    
    def get_signature(self) -> str:
        return self.signature