import json

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email
        }

# user = User(username="hwf", password="666666", email="kkk@qq.com")

# print(user.dict())

# print(json.dumps(user.dict()))