from models.event_model import EventModel
from models.ticket_model import TicketModel
from models.ticket_type_model import TicketTypeModel


class TicketProcessor:
    def process_record(self, ticket_record):
        created_tickets = []
        ticket_quantity = int(ticket_record.pop('quantity'))
        event_record = EventModel().get_event(ticket_record.get('event_id'))
        ticket_record['event_title'] = event_record.get('title')
        ticket_record['event_description'] = event_record.get('description')
        ticket_type_record = TicketTypeModel().get_ticket_type(ticket_record.get('ticket_type_id'))
        ticket_record['ticket_type_title'] = ticket_type_record.get('title')
        ticket_record['ticket_type_description'] = ticket_type_record.get('description')
        ticket_record['price'] = ticket_type_record.get('price')
        for i in range(ticket_quantity):
            current_ticket = TicketModel().create_ticket(ticket_record.copy())
            created_tickets.append(current_ticket)
        return created_tickets
