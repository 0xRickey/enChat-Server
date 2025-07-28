import time

class Message():
    def __init__(self, msg: str, timestamp: int = int(time.time())):
        self.msg = msg
        self.timestamp = timestamp

    def as_dict(self) -> dict:
        return {
            "MESSAGE": self.msg,
            "TIMESTAMP": self.timestamp
        } 