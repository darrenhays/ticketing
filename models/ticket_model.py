import logging
from boto3.dynamodb.conditions import Key
from models.abstract_model import AbstractModel
from settings import TICKETS_TABLE_NAME

logger = logging.getLogger()


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

    def get_tickets_by_event(self, event_id):
        logger.info("########## {} get_tickets_by_event ##########".format(self.__class__.__name__))
        logger.info("event_id: {}".format(event_id))
        key = Key('event_id').eq(event_id)
        try:
            response = self.table.query(IndexName='event_id_index', KeyConditionExpression=key)
            return response.get('Items')
        except Exception as e:
            logger.error(e)
            return []

    def get_tickets_by_ticket_type(self, ticket_type_id):
        logger.info("########## {} get_tickets_by_ticket_type ##########".format(self.__class__.__name__))
        logger.info("ticket_type_id: {}".format(ticket_type_id))
        key = Key('ticket_type_id').eq(ticket_type_id)
        try:
            response = self.table.query(IndexName='ticket_type_id_index', KeyConditionExpression=key)
            return response.get('Items')
        except Exception as e:
            logger.error(e)
            return []
