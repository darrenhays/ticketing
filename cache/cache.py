import redis
from settings import CACHE_HOST, CACHE_PORT


class Cache:
    def __init__(self):
        self.client = redis.Redis(host=CACHE_HOST, port=CACHE_PORT)

    def set(self, key, value, expiration=900):
        self.client.set(key, value, ex=expiration)

    def get(self, key):
        return self.client.get(key)
