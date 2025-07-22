import json

class Response:
    def __init__(self,
        status: str,
        payload: dict,
        metadata: dict,
        signature: str,
        response_id: str
    ):
        self.status = status
        self.payload = payload
        self.metadata = metadata
        self.signature = signature
        self.response_id = response_id

    def get_status(self):
        return self.status

    def get_payload(self):
        return self.payload

    def get_metadata(self):
        return self.metadata

    def get_response_id(self):
        return self.response_id
    
    def get_signature(self):
        return self.signature
    
    def as_dict(self):
        return {
            "STATUS": self.status,
            "PAYLOAD": self.payload,
            "METADATA": self.metadata,
            "SIGNATURE": self.signature
        }

    def as_bytes(self):
        return json.dumps(self.as_dict()).encode()