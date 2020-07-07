import json

class User:
    __attributes = {}
    sensitive_attributes = ['password']
    allowed_attributes = [
        'id',
        'email',
        'first_name',
        'last_name'
    ] + sensitive_attributes

    def __init__(self, attributes={}):
        self.load(attributes)

    def __getattr__(self, key):
        return self.__attributes[key]

    def __setattr__(self, key, value):
        if key in self.allowed_attributes:
            self.__attributes[key] = value

    @property
    def __dict__(self):
        return self.__attributes

    def load(self, attributes):
        for key, value in attributes.items():
            if key in self.allowed_attributes:
                self.__attributes[key] = value

    @property
    def attributes(self):
        return self.__dict__

    def jsonify(self):
        attributes = self.__dict__
        for attribute in self.sensitive_attributes:
            attributes.pop(attribute, None)
        return json.dumps(attributes)
