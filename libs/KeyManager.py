import os, dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

class KeyManager:
    def __init__(self):
        if dotenv.load_dotenv():
            self.private_key = os.getenv("PRIVATE_KEY")
            self.public_key = os.getenv("PUBLIC_KEY")
        else:
            self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            self.public_key = self.private_key.public_key()

            priv_key_pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()

            pub_key_pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()

            dotenv.set_key(".env", "PRIVATE_KEY", priv_key_pem)
            dotenv.set_key(".env", "PUBLIC_KEY", pub_key_pem)

    def get_private_key(self) -> RSAPrivateKey:
        return self.private_key
    
    def get_public_key(self) -> RSAPublicKey:
        return self.public_key
    
    def get_pub_key_PEM(self) -> str:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
