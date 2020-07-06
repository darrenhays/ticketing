import json

class User:
    sensitive_attributes = ['password']

    def __init__(self, attributes={}):
        self.load(attributes)

    @property
    def __dict__(self):
        attributes = {
            'id': self.id,
            'email': self.email,
            'password': self.__password,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
        # strip sensitive attributes
        for attribute in self.sensitive_attributes:
            attributes.pop(attribute)
        return attributes

    def load(self, attributes):
        self.id = attributes.get('id')
        self.email = attributes.get('email')
        self.__password = attributes.get('password')
        self.first_name = attributes.get('first_name')
        self.last_name = attributes.get('last_name')

    @property
    def attributes(self):
        return self.__dict__

    def jsonify(self):
        return json.dumps(self.__dict__)

    def password(self):
        return self.__password
