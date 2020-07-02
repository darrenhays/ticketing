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
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    def load(self, attributes):
        self.id = attributes.get('id')
        self.email = attributes.get('email')
        self.password = attributes.get('password')
        self.first_name = attributes.get('first_name')
        self.last_name = attributes.get('last_name')

    @property
    def attributes(self):
        return self.__dict__

    def jsonify(self):
        return json.dumps(self.__dict__)
