import os, json

import libs.constants as constants

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as padding_primitives

from libs.KeyManager import KeyManager
from libs.response.Response import Response

class Encryptor:
    def __init__(self, keyManager: KeyManager):
        self.keyManager = keyManager

    def RSA_encrypt(self, response: Response, PEM_pub_key: str) -> bytes:
        """
        Encrypts a Response object using RSA encryption.
        Args:
            response: The response to encrypt.
            PEM_pub_key: The public key to use for encryption.
        Returns:
            The encrypted response in bytes.
        """
        # return self.keyManager.get_public_key().encrypt(
        #     response.as_bytes(),
        #     padding.OAEP(
        #         mgf=padding.MGF1(algorithm=hashes.SHA256()),
        #         algorithm=hashes.SHA256(),
        #         label=None
        #     )
        # )
        pass
    
    def AES_encrypt(self,
        response: Response,
        session_key: bytes,
        init_vec: bytes = os.urandom(constants.AES_BLOCK_SIZE_BYTES)
    ) -> bytes:
        """
        Encrypts a Response object using AES + CBC encryption.
        Args:
            response: The response to encrypt.
            session_key: The AES session key to use for encryption.
        Returns:
            The encrypted response in bytes.
        """
        # Load data into padder object and then call finalise to pad
        # the data to be a multiple of the block size
        padder = padding_primitives.PKCS7(constants.AES_BLOCK_SIZE_BITS).padder()
        padded_data = padder.update(response.as_bytes()) + padder.finalize()

        # Create the AESCBC cipher object that will be
        # used to encrypt the data
        cipher = Cipher(algorithms.AES(session_key), modes.CBC(init_vec))
        encryptor = cipher.encryptor()

        # Encrypt the data
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        AES_encrypted_response = {
            "CIPHERTEXT": ciphertext,
            "IV": init_vec.decode()
        }

        AES_encrypted_json_str = json.dumps(AES_encrypted_response)

        return AES_encrypted_json_str.encode()