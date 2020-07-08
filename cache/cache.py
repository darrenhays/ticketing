import redis


class Cache:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379) #FIXME place in settings

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)
