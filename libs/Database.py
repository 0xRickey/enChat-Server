import json, hashlib, os, time

from libs.Message import Message

class Database:
    def __init__(self):
        try:
            with open("database.json", "r") as f:
                database: dict = json.loads(f.read())

            self.users: dict = database["USERS"]
            self.chats: dict = database["CHATS"]
        except FileNotFoundError:
            self.users: dict = {}
            self.chats: dict = {}

    def does_user_exist(self, username: str):
        return username in self.users.keys()
    
    def add_user(self, username: str, password: str, pubKey: str):
        THIRTY_TWO_BYTES = 32
        # Generate 32 random bytes to use a password salt
        salt: str = os.urandom(THIRTY_TWO_BYTES).hex()
        saltedPassword: str = salt + password
        saltedPwdHash: str = hashlib.sha256(saltedPassword.encode()).hexdigest()

        self.users[username] = {
            "SALT": salt,
            "PASSWORD": saltedPwdHash,
            "PUBLIC_KEY": pubKey
        }

    def get_user_pub_key(self, username: str) -> str:
        return self.users[username]["PUBLIC_KEY"]

    def try_user_login(self, username: str, password: str):
        salt: str = self.users[username]["SALT"]
        saltedPassword: str = salt + password
        saltedPwdHash: str = hashlib.sha256(saltedPassword.encode()).hexdigest()

        return saltedPwdHash == self.users[username]["PASSWORD"]

    def write_to_db(self):
        with open("database.json", "w") as f:
            f.write(json.dumps({"USERS": self.users, "CHATS": self.chats}, indent=4))

    def add_msg(self, fromUser: str, toUser: str, msg: str, timestamp: int):
        chatKey = f"{fromUser}-{toUser}"
        newMsg: Message = Message(msg=msg, timestamp=timestamp)

        try:
            chatMessages: list[dict] = self.chats[chatKey]["MESSAGES"]
            chatMessages.append(newMsg.as_dict())
        except KeyError:
            self.chats[chatKey] = {
                "LAST_GET": 0,
                "MESSAGES": [newMsg.as_dict()]
            }

        self.write_to_db()

    def get_messages(self, fromUser: str, toUser: str) -> list[Message] | None:
        try:
            chatKey = f"{fromUser}-{toUser}"
            newMsgs: list[Message] = []
            lastGet: int = self.chats[chatKey]["LAST_GET"]
            for msg in self.chats[chatKey]["MESSAGES"]:
                if msg["TIMESTAMP"] > lastGet:
                    newMsgs.append(Message(msg["MESSAGE"], msg["TIMESTAMP"]))
            
            self.chats[chatKey]["LAST_GET"] = int(time.time())
            
            self.write_to_db()
            return newMsgs
        except KeyError:
            return None