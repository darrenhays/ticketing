import redis
from settings import CACHE_HOST, CACHE_PORT
'''
Cache is no longer being used
Keeping files around for reference and future development
'''


class Cache:
    def __init__(self):
        self.client = redis.Redis(host=CACHE_HOST, port=CACHE_PORT, socket_connect_timeout=2)

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, expiration=900):
        self.client.set(key, value, ex=expiration)

    def delete(self, key):
        self.client.delete(key)
