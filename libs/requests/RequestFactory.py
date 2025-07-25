import json
from libs.requests.Request import Request
from libs.requests.EncryptedRequest import EncryptedRequest
from pprint import pprint

class RequestFactory:
    @staticmethod
    def request_from_bytes(
        msg: bytes,
        signature: str,
        pubKey: str,
        init_vec: str,
        sessionId: int,
        returnAddr: tuple[str, int]
    ) -> Request:
        msgJsonStr: str = msg.decode()
        msgDict: dict = json.loads(msgJsonStr)
        
        return Request(
            command=msgDict["COMMAND"],
            payload=msgDict["PAYLOAD"],
            metadata=msgDict["METADATA"],
            signature=signature,
            pubKey=pubKey,
            init_vec=init_vec,
            sessionId=sessionId,
            returnAddr=returnAddr
        )

    @staticmethod
    def request_from_compressed_json(
        jsonStr: str,
        signature: str,
        pubKey: str,
        init_vec: str,
        returnAddr: tuple[str, int]
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
            init_vec=init_vec,
            returnAddr=returnAddr
        )

    @staticmethod
    def encrypted_req_from_bytes(
        encryptedRequest: bytes,
        returnAddr: tuple[str, int]
    ) -> EncryptedRequest:
        encryptedReqDict = json.loads(encryptedRequest.decode())
        pprint(encryptedReqDict)
        return EncryptedRequest(
            encryptedReqDict["CIPHERTEXT"],
            encryptedReqDict["SIGNATURE"],
            encryptedReqDict["PUBLIC_KEY"],
            encryptedReqDict["IV"],
            encryptedReqDict["SESSION_ID"],
            returnAddr
        )