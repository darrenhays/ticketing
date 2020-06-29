import logging
from datetime import datetime
from models.abstract_model import AbstractModel

logger = logging.getLogger()


class SessionModel(AbstractModel):
    table_name = 'Sessions'

    def create_session(self):
        item = {'created': str(datetime.now())}
        return self.insert(item)

    def get_session(self, session_id):
        return self.get(session_id)

    def refresh_session(self, session_id):
        updated_attribute = {'created': datetime.now()}
        return self.update(session_id, updated_attribute)
