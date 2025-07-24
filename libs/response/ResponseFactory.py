from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from libs.response.Response import Response
from libs.KeyManager import KeyManager

class ResponseFactory:
    @staticmethod
    def create_response(
        status: str,
        payload: dict,
        metadata: dict,
        keyManager: KeyManager,
    ) -> Response:
        msg  = {
            "STATUS": status,
            "PAYLOAD": payload,
            "METADATA": metadata,
        }

        signature: str = keyManager.sign_message(msg)
        rsaPubKey: RSAPublicKey = keyManager.get_public_key()

        return Response(status, payload, metadata, signature, rsaPubKey)
