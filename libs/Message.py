import time

class Message():
    def __init__(self, msg: str) -> None:
        self.msg = msg
        self.timestamp = int(time.time())

    def as_dict(self) -> dict:
        return {
            "MESSAGE": self.msg,
            "TIMESTAMP": self.timestamp
        } 