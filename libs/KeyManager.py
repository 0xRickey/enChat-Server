import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class KeyManager:
    @staticmethod
    def generate_server_key_pair():
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        # read json database and serialise it to a dictionary
        try:
            with open("keypair.json", "r") as f:
                keys_db = json.load(f)
        except FileNotFoundError:
            keys_db = {}
        
        # serialise the private and public keys to PEM (human readable format)
        keys_db["private_key"] = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        keys_db["public_key"] = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        # Update by rewriting the local database
        with open("keypair.json", "w") as f:
            json.dump(keys_db, f, indent=4)