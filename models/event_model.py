from models.abstract_model import AbstractModel
from settings import EVENTS_TABLE_NAME


class EventModel(AbstractModel):
    table_name = EVENTS_TABLE_NAME
    required_attributes = [
        'title',
        'user_id',
        'capacity',
        'status'
    ]
    optional_attributes = [
        'description'
    ]

    def create_event(self, attributes={}):
        return self.insert(attributes)

    def get_event(self, event_id):
        return self.get(event_id)

    def delete_event(self, event_id):
        return self.delete(event_id)

    def update_event(self, event_id, updated_attributes):
        return self.update(event_id, updated_attributes)
