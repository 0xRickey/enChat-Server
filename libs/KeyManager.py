import json

from hashlib import sha256

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

class KeyManager:
    def __init__(self):
        try:
            with open("keys/private_key.der", "rb") as f:
                print("Loading private key from DER file")
                privKeyAsbytes = f.read()
                self.private_key = serialization.load_der_private_key(
                    privKeyAsbytes, password=None
                )
                self.public_key  = self.private_key.public_key()
        except FileNotFoundError:
            print("No private key found. Generating a new one.")
            
            self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            self.public_key = self.private_key.public_key()

            with open("keys/private_key.der", "wb") as f:
                f.write(self.private_key.private_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            with open("keys/public_key.der", "wb") as f:
                f.write(self.public_key.public_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

    def sign_message(self, msg: dict) -> str:
        msgBytes = json.dumps(msg).encode()
        msgHash  = sha256(msgBytes).hexdigest().encode()
        
        signature = self.private_key.sign(
            msgHash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return signature.hex()

    def get_private_key(self) -> RSAPrivateKey:
        return self.private_key
    
    def get_public_key(self) -> RSAPublicKey:
        return self.public_key
    
    def get_PEM_pub_key(self) -> str:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
