import json
from libs.KeyManager import KeyManager
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from libs.requests.Request import Request
from libs.requests.RequestFactory import RequestFactory

class Decryptor:
    def __init__(self, keyManager: KeyManager):
        self.keyManager = keyManager

    def decrypt_message(self, bytes_msg: bytes) -> Request:
        try:
            return self.RSA_decrypt(bytes_msg)
        except Exception as e:
            return self.AES_decrypt(bytes_msg)

    def RSA_decrypt(self, encryptedRequest: bytes) -> Request:
        """
        Decrypts the encrypted request using the server's
        RSA private key.
        """
        decryptedRequest = self.keyManager.get_private_key().decrypt(
            encryptedRequest,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        reqJsonStr = json.loads(decryptedRequest.decode())

        return RequestFactory.request_from_jsonstr(reqJsonStr)

    def AES_decrypt(
        self,
        encryptedRequest: bytes,
        sessionKey: bytes,
        init_vector: bytes
    ) -> Request:
        """
        Decrypts an encrypted request using AESCBC, an initialisation
        vector and a session key that was previously shared with the
        server.
        """
        pass
