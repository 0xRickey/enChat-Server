import json
from libs.KeyManager import KeyManager
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from libs.requests.Request import Request
from libs.requests.EncryptedRequest import EncryptedRequest
from libs.requests.RequestFactory import RequestFactory

class Decryptor:
    def __init__(self, keyManager: KeyManager):
        self.keyManager = keyManager

    def decrypt_request(self, encryptedRequest: EncryptedRequest) -> Request:
        if encryptedRequest.get_init_vec() != "":
            return self.AES_decrypt(encryptedRequest)
        else:
            return self.RSA_decrypt(encryptedRequest)

    def RSA_decrypt(self, encryptedRequest: EncryptedRequest) -> Request:
        """
        Decrypts the encrypted request using the server's
        RSA private key.
        """
        ciphertext = encryptedRequest.get_ciphertext()
        decryptedRequest = self.keyManager.get_private_key().decrypt(
            ciphertext.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        reqJsonStr = decryptedRequest.decode()
        signature = encryptedRequest.get_signature()
        publicKey = encryptedRequest.get_PEM_public_key()
        init_vec = encryptedRequest.get_init_vec()

        return RequestFactory.request_from_compressed_json(
            reqJsonStr, signature, publicKey, init_vec
        )

    def AES_decrypt(self, encryptedRequest: EncryptedRequest) -> Request:
        """
        Decrypts an encrypted request using AESCBC, an initialisation
        vector and a session key that was previously shared with the
        server.
        """
        pass
