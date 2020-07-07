from hashlib import sha256
from settings import SALT


class Password:
    def __init__(self, password):
        password = password + SALT
        self.__hash = sha256(password.encode('utf-8')).hexdigest()

    def __eq__(self, other):
        return other == self.__hash

    def __str__(self):
        return self.__hash
