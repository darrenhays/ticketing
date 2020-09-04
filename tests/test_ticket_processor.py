import unittest
from objects.ticket_processor import TicketProcessor
from unittest.mock import patch


class TestTicketProcessor(unittest.TestCase):
    def test_ticket_processor_passing_in_an_empty_dictionary_returns_an_empty_list(self):
        assert not TicketProcessor().process_record({})

    @patch('objects.ticket_processor.EventModel.get_event')
    @patch('objects.ticket_processor.TicketTypeModel.get_ticket_type')
    @patch('objects.ticket_processor.TicketModel.create_ticket')
    def test_processing_two_tickets(self, mock_create_ticket, mock_get_ticket_type, mock_get_event):
        # mock
        mock_get_event.return_value = {
            'title': 'test event title',
            'description': 'test event description'
        }
        mock_get_ticket_type.return_value = {
            'title': 'test ticket type title',
            'description': 'test ticket type description',
            'price': '7'
        }
        mock_create_ticket.return_value = {'mock_ticket_id': "7"}

        # testing
        ticket_record = {'event_id': '1', 'ticket_type_id': '2', 'quantity': "2"}
        assert len(TicketProcessor().process_record(ticket_record)) == 2
