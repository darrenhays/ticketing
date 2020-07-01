import logging
from datetime import datetime, timedelta
from models.abstract_model import AbstractModel

logger = logging.getLogger()


class SessionModel(AbstractModel):
    table_name = 'Sessions'

    def create_session(self, user_id):
        expiration = str(datetime.now() + timedelta(minutes=15))
        item = {
            'user_id': user_id,
            'expiration': expiration
            }
        return self.insert(item)

    def get_session(self, session_id):
        return self.get(session_id)

    def refresh_session(self, session_id):
        expiration = str(datetime.now() + timedelta(minutes=15))
        updated_attributes = {'expiration': expiration}
        return self.update(session_id, updated_attributes)
