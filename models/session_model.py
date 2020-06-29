import logging
from datetime import datetime
from models.abstract_model import AbstractModel

logger = logging.getLogger()


class SessionModel(AbstractModel):
    def __init__(self):
        self.table_name = 'Sessions'
        super().__init__()

    def create_session(self):
        now = datetime.now()
        item = {
            'creation_time': str(now)
        }
        return self.insert(item)

    def get_session(self, session_id):
        return self.get(session_id)

    def refresh_session(self, session_id):
        now = datetime.now()
        updated_attribute = {'creation_time': now}
        return self.update(session_id, updated_attribute)
