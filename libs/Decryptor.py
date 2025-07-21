import json
from libs.KeyManager import KeyManager
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes

class Decryptor:
    def __init__(self, keyManager: KeyManager):
        self.keyManager = keyManager

    def decrypt_message(self, bytes_msg: bytes) -> bytes:
        try:
            return self.RSA_decrypt(bytes_msg)
        except Exception as e:
            return self.AES_decrypt(bytes_msg)

    def RSA_decrypt(self, encrypted_msg: bytes) -> bytes:
        return self.keyManager.get_private_key().decrypt(
            encrypted_msg,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def AES_decrypt(self, bytes_msg: bytes) -> bytes:
        # TODO: Add AES decryption
        pass