from hashlib import sha256
from settings import SALT


class Encryptor:
    def __init__(self, password):
        password = password + SALT
        self.hash = sha256(password.encode('utf-8')).hexdigest()
