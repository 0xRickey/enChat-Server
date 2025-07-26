import json, hashlib, os

class Database:
    def __init__(self):
        with open("database.json", "r") as f:
            database: dict = json.loads(f.read())

        self.users: dict = database["USERS"]

    def does_user_exist(self, username: str):
        return username in self.users.keys()
    
    def add_user(self, username: str, password: str):
        THIRTY_TWO_BYTES = 32
        # Generate 32 random bytes to use a password salt
        salt: str = os.urandom(THIRTY_TWO_BYTES).hex()
        saltedPassword: str = salt + password
        saltedPwdHash: str = hashlib.sha256(saltedPassword.encode()).hexdigest()

        self.users[username] = {
            "SALT": salt,
            "PASSWORD": saltedPwdHash
        }

    def write_to_db(self):
        with open("database.json", "w") as f:
            f.write(json.dumps({"USERS": self.users}, indent=4))