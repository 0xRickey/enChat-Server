import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class KeyManager:
    @staticmethod
    def generate_server_key_pair():
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        
        # serialise the private and public keys to PEM (human readable format)
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        # Update by rewriting the .env file
        with open(".env", "w") as f:
            f.write(f"PRIVATE_KEY={private_key_pem}\n")
            f.write(f"PUBLIC_KEY={public_key_pem}\n")
