from models.abstract_model import AbstractModel
from settings import TICKETS_TABLE_NAME


class TicketModel(AbstractModel):
    table_name = TICKETS_TABLE_NAME
    required_attributes = [
        'event_id',
        'event_title',
        'event_description',
        'ticket_type_id',
        'ticket_type_title',
        'ticket_type_description',
        'amount_paid'
    ]

    def create_ticket(self, attributes):
        return self.insert(attributes)

    def get_ticket(self, ticket_id):
        return self.get(ticket_id)

    def delete_ticket(self, ticket_id):
        return self.delete(ticket_id)

    def update_ticket(self, ticket_id, updated_attributes):
        return self.update(ticket_id, updated_attributes)
