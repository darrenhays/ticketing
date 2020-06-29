import json

class User:
    def __init__(self, attributes={}):
        self.load(attributes)

    @property
    def __dict__(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
        }

    def load(self, attributes):
        self.id = attributes.get('id')
        self.email = attributes.get('email')
        self.password = attributes.get('password')

    @property
    def attributes(self):
        return self.__dict__

    def jsonify(self):
        return json.dumps(self.__dict__)
