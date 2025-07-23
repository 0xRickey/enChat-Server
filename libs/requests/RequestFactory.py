import json
from libs.requests.Request import Request

class RequestFactory:
    @staticmethod
    def request_from_jsonstr(jsonStr: str) -> Request:
        requestDict: dict = json.loads(jsonStr)

        return Request(
            command=requestDict["MESSAGE"]["COMMAND"],
            payload=requestDict["MESSAGE"]["PAYLOAD"],
            metadata=requestDict["MESSAGE"]["METADATA"],
            signature=requestDict["SIGNATURE"]
        )