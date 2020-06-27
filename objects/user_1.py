import json

class User:
    def __init__(self, id=None, email=None, password=None):
        self.id = id
        self.email = email
        self.password = password

    @property
    def __dict__(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
        }

    def jsonify(self):
        return json.dumps(self.__dict__)
