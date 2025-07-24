from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class EncryptedRequest:
    def __init__(
        self,
        ciphertext: str,
        signature: str,
        publicKey: str
    ):
        self.ciphertext = ciphertext,
        self.signature = signature,
        self.publicKey = publicKey

    def get_ciphertext(self) -> str:
        return self.ciphertext
    
    def get_signature(self) -> str:
        return self.signature
    
    def get_PEM_public_key(self) -> str:
        return self.publicKey
    
    def get_public_key(self) -> rsa.RSAPublicKey:
        """
        Serialises the stored PEM public key
        into an RSAPublicKey object
        """
        return serialization.load_pem_public_key(
            self.publicKey.encode()
        )
