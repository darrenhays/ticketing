from models.abstract_model import AbstractModel
from settings import TICKET_TYPES_TABLE_NAME


class TicketTypeModel(AbstractModel):
    table_name = TICKET_TYPES_TABLE_NAME
    required_attributes = [
        'title',
        'event_id',
        'limit',
        'price'
    ]
    optional_attributes = [
        'description',
    ]

    def create_ticket_type(self, attributes):
        return self.insert(attributes)

    def get_ticket_type(self, ticket_type_id):
        return self.get(ticket_type_id)

    def delete_ticket_type(self, ticket_type_id):
        return self.delete(ticket_type_id)

    def update_ticket_type(self, ticket_type_id, updated_attributes):
        return self.update(ticket_type_id, updated_attributes)
