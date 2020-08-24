import logging
from models.event_model import EventModel
from models.ticket_model import TicketModel
from models.ticket_type_model import TicketTypeModel

logger = logging.getLogger()


class TicketChecker:
    def __init__(self, ticket_attributes): #FIXME this should receive a ticket object instead
        logger.info("########## {} __init__ ##########".format(self.__class__.__name__))
        logger.info("ticket_attributes: {}".format(ticket_attributes))
        self.event_id = ticket_attributes.get('event_id')
        self.ticket_type_id = ticket_attributes.get('ticket_type_id')

    def is_oversold(self):
        logger.info("########## {} is_oversold ##########".format(self.__class__.__name__))
        event_ticket_total = len(TicketModel().get_tickets_by_event(self.event_id))
        event_capacity = int(EventModel().get_event(self.event_id).get('capacity'))
        ticket_type_ticket_total = len(TicketModel().get_tickets_by_ticket_type(self.ticket_type_id))
        ticket_type_limit = int(TicketTypeModel().get_ticket_type(self.ticket_type_id).get('limit'))
        return event_ticket_total > event_capacity or ticket_type_ticket_total > ticket_type_limit
