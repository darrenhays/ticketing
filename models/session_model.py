import logging
from models.abstract_model import AbstractModel
from settings import SESSIONS_TABLE_NAME

logger = logging.getLogger()


class SessionModel(AbstractModel):
    table_name = SESSIONS_TABLE_NAME

    def create_session(self, user_id):
        item = {
            'user_id': user_id
        }
        return self.insert(item)

    def delete_session(self, session_id):
        return self.delete(session_id)

    def get_session(self, session_id):
        return self.get(session_id)
