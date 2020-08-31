import unittest
from objects.ticket import Ticket
from objects.ticket_checker import TicketChecker
from unittest.mock import patch


class TestTicketChecker(unittest.TestCase):

    @patch('models.ticket_model.TicketModel.get_tickets_by_event')
    @patch('models.event_model.EventModel.get_event')
    @patch('models.ticket_model.TicketModel.get_tickets_by_ticket_type')
    @patch('models.ticket_type_model.TicketTypeModel.get_ticket_type')
    def test_is_oversold_when_ticket_is_oversold(self, mock_get_ticket_type, mock_get_tickets_by_ticket_type, mock_get_event, mock_get_tickets_by_event):
        ticket_attributes = {
            "event_id": "123",
            "ticket_type_id": "123"
        }
        ticket = Ticket(ticket_attributes)

        mock_get_tickets_by_event.return_value = [
            {"id": "1"},
            {"id": "2"}
        ]
        mock_get_event.return_value = {"capacity": "1"}
        mock_get_tickets_by_ticket_type.return_value = [
            {"id": "1"},
            {"id": "2"}
        ]
        mock_get_ticket_type.return_value = {"limit": "1"}

        is_oversold_return = TicketChecker(ticket).is_oversold()

        assert is_oversold_return

    @patch('models.ticket_model.TicketModel.get_tickets_by_event')
    @patch('models.event_model.EventModel.get_event')
    @patch('models.ticket_model.TicketModel.get_tickets_by_ticket_type')
    @patch('models.ticket_type_model.TicketTypeModel.get_ticket_type')
    def test_is_oversold_when_ticket_is_not_oversold(self, mock_get_ticket_type, mock_get_tickets_by_ticket_type, mock_get_event, mock_get_tickets_by_event):
        ticket_attributes = {
            "event_id": "123",
            "ticket_type_id": "123"
        }
        ticket = Ticket(ticket_attributes)

        mock_get_tickets_by_event.return_value = [
            {"id": "1"},
            {"id": "2"}
        ]
        mock_get_event.return_value = {"capacity": "3"}
        mock_get_tickets_by_ticket_type.return_value = [
            {"id": "1"},
            {"id": "2"}
        ]
        mock_get_ticket_type.return_value = {"limit": "3"}

        is_oversold_return = TicketChecker(ticket).is_oversold()

        assert not is_oversold_return

    @patch('models.ticket_model.TicketModel.get_tickets_by_event')
    @patch('models.event_model.EventModel.get_event')
    @patch('models.ticket_model.TicketModel.get_tickets_by_ticket_type')
    @patch('models.ticket_type_model.TicketTypeModel.get_ticket_type')
    def test_is_oversold_when_event_and_ticket_type_do_not_exist(self, mock_get_ticket_type, mock_get_tickets_by_ticket_type, mock_get_event, mock_get_tickets_by_event):
        ticket_attributes = {
            "event_id": "123",
            "ticket_type_id": "123"
        }
        ticket = Ticket(ticket_attributes)

        mock_get_tickets_by_event.return_value = []
        mock_get_event.return_value = {}
        mock_get_tickets_by_ticket_type.return_value = []
        mock_get_ticket_type.return_value = {}

        is_oversold_return = TicketChecker(ticket).is_oversold()

        assert is_oversold_return
