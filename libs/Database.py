import json

class Database:
    def __init__(self):
        with open("database.json", "r") as f:
            database: dict = json.loads(f.read())

        self.users: dict = database["USERS"]

    def does_user_exist(self, username: str):
        return username in self.users.keys()