import json
import logging
import uuid
from cache.cache import Cache

logger = logging.getLogger()


class SessionModel:
    def __init__(self):
        self.cache = Cache()

    def create_session(self, user_id):
        id = str(uuid.uuid4())
        item = {
            'id': id,
            'user_id': user_id
        }
        self.cache.set(id, json.dumps(item))
        return item

    def delete_session(self, session_id):
        self.cache.delete(session_id)

    def get_session(self, session_id):
        return json.loads(self.cache.get(session_id))
