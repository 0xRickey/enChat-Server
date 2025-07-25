import base64, json

import libs.constants as constants

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as padding_asymmetric
from cryptography.hazmat.primitives import padding as padding_primitives
from cryptography.hazmat.primitives import hashes

from libs.KeyManager import KeyManager
from libs.requests.Request import Request
from libs.requests.EncryptedRequest import EncryptedRequest
from libs.requests.RequestFactory import RequestFactory
from libs.sessions.Session import Session
from libs.sessions.SessionsLog import SessionsLog

class Decryptor:
    def __init__(self, keyManager: KeyManager, sessionsLog: SessionsLog):
        self.keyManager = keyManager
        self.sessionsLog = sessionsLog

    def decrypt_request(self, encryptedRequest: EncryptedRequest) -> Request:
        if encryptedRequest.get_init_vec() != "":
            print("The Request is AES Encrypted, decrypting with associated session key...")
            sessionId: int = encryptedRequest.get_session_id()
            session: Session = self.sessionsLog.get_session(sessionId)
            sessionKey: bytes = session.get_expanded_session_key()
            return self.AES_decrypt(encryptedRequest, sessionKey)
        else:
            print("The Request is RSA Encrypted, decrypting with server's private key...")
            return self.RSA_decrypt(encryptedRequest)

    def RSA_decrypt(self, encryptedRequest: EncryptedRequest) -> Request:
        """
        Decrypts the encrypted request using the server's
        RSA private key.
        """
        ciphertext = base64.b64decode(
            encryptedRequest.get_ciphertext().encode('utf-8')
        )

        decryptedRequest = self.keyManager.get_private_key().decrypt(
            ciphertext,
            padding_asymmetric.OAEP(
                mgf=padding_asymmetric.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        reqJsonStr = decryptedRequest.decode()
        signature = encryptedRequest.get_signature()
        publicKey = encryptedRequest.get_PEM_public_key()
        init_vec = encryptedRequest.get_init_vec()

        return RequestFactory.request_from_compressed_json(
            reqJsonStr,
            signature,
            publicKey,
            init_vec,
            encryptedRequest.get_return_addr()
        )

    def AES_decrypt(
        self,
        encryptedRequest: EncryptedRequest,
        sessionKey: bytes
    ) -> Request:
        """
        Decrypts an encrypted request using AESCBC, an initialisation
        vector and a session key that was previously shared with the
        server.
        """
        ciphertext = encryptedRequest.get_ciphertext() # UTF-8 String of base64 bytes
        ciphertext = ciphertext.encode() # UTF-8 string of base64 bytes -> base64 bytes
        ciphertext = base64.b64decode(ciphertext) # base64 bytes -> regular mumbo jumbo

        init_vec = encryptedRequest.get_init_vec() # UTF-8 string of base64 bytes
        init_vec = init_vec.encode() # UTF-8 string or base64 bytes -> base64 bytes
        init_vec = base64.decode(ciphertext) # base64 bytes -> original mumbo jumbo

        aesCipher = Cipher(
            algorithm=algorithms.AES(sessionKey),
            mode=modes.CBC(init_vec)
        )

        aesDecryptor = aesCipher.decryptor()

        paddedMsg = aesDecryptor.update(ciphertext) + aesDecryptor.finalize()

        unpadder = padding_primitives.PKCS7(constants.AES_BLOCK_SIZE_BITS).unpadder()

        msgJsonBytes: bytes = unpadder.update(paddedMsg) + unpadder.finalize()
        msgJsonStr: str = msgJsonBytes.decode()
        msg: dict = json.loads(msgJsonStr)

        request = RequestFactory.request_from_bytes(
            msgJsonBytes,
            encryptedRequest.get_signature(),
            encryptedRequest.get_PEM_public_key(),
            encryptedRequest.get_init_vec(),
            encryptedRequest.get_session_id(),
            encryptedRequest.get_return_addr()
        )

        return request
