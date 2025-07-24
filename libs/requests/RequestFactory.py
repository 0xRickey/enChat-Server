import json
from libs.requests.Request import Request
from libs.requests.EncryptedRequest import EncryptedRequest

class RequestFactory:    
    @staticmethod
    def request_from_compressed_json(
        jsonStr: str,
        signature: str,
        pubKey: str,
        init_vec: str
    ) -> Request:
        msgDict: dict = json.loads(jsonStr)
        command = msgDict["C"]
        payload = msgDict["P"]
        metadata = msgDict["T"]

        return Request(
            command=command,
            payload=payload,
            metadata=metadata,
            signature=signature,
            pubKey=pubKey,
            init_vec=init_vec
        )

    @staticmethod
    def encrypted_req_from_bytes(encryptedRequest: bytes) -> EncryptedRequest:
        encryptedReqDict = json.loads(encryptedRequest.decode())
        return EncryptedRequest(
            encryptedReqDict["CIPHERTEXT"],
            encryptedReqDict["SIGNATURE"],
            encryptedReqDict["PUBLIC_KEY"],
            encryptedReqDict["IV"]
        )