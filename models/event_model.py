import logging
from boto3.dynamodb.conditions import Key
from models.abstract_model import AbstractModel
from settings import EVENTS_TABLE_NAME

logger = logging.getLogger()


class EventModel(AbstractModel):
    table_name = EVENTS_TABLE_NAME
    required_attributes = [
        'title',
        'user_id',
        'capacity'
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

    def get_number_of_tickets_by_event(self, event_id):
        logger.info("########## {} get_total_by_event ##########".format(self.__class__.__name__))
        logger.info("event_id: {}".format(event_id))
        key = Key('event_id').eq(event_id)
        try:
            response = self.table.query(IndexName='event_id_index', KeyConditionExpression=key)
            return int(response.get('Count'))
        except Exception as e:
            logger.error(e)
            return {}

    def get_number_of_tickets_by_ticket_type(self, ticket_type_id):
        logger.info("########## {} get_total_by_ticket_type ##########".format(self.__class__.__name__))
        logger.info("ticket_type_id: {}".format(ticket_type_id))
        key = Key('ticket_type_id').eq(ticket_type_id)
        try:
            response = self.table.query(IndexName='ticket_type_id_index', KeyConditionExpression=key)
            return int(response.get('Count'))
        except Exception as e:
            logger.error(e)
            return {}