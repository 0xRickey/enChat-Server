import uuid, json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from libs.response.Response import Response
from libs.KeyManager import KeyManager

class ResponseFactory:
    @staticmethod
    def create_response(
        status: str,
        payload: dict,
        metadata: dict,
        keyManager: KeyManager
    ) -> Response:
        response_id = str(uuid.uuid4())
        signature = keyManager.get_private_key().sign(
            json.dumps(payload).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return Response(status, payload, metadata, signature, response_id)
