from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class EncryptedRequest:
    def __init__(
        self,
        ciphertext: str,
        signature: str,
        publicKey: str,
        init_vec: str,
        session_id: int,
        returnAddr: tuple[str, int]
    ):
        self.ciphertext = ciphertext
        self.signature = signature
        self.publicKey = publicKey
        self.init_vec = init_vec
        self.session_id = session_id
        self.returnAddr = returnAddr

    def get_ciphertext(self) -> str:
        return self.ciphertext
    
    def get_signature(self) -> str:
        return self.signature
    
    def get_init_vec(self) -> str:
        return self.init_vec
    
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
    
    def get_return_addr(self) -> tuple[str, int]:
        return self.returnAddr

    def get_session_id(self) -> int:
        return self.session_id