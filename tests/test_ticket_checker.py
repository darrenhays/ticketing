import unittest
from objects.ticket import Ticket
from objects.ticket_checker import TicketChecker
from unittest.mock import patch


class TestTicketChecker(unittest.TestCase):
    @patch('objects.ticket_checker.TicketModel.get_tickets_by_event')
    @patch('objects.ticket_checker.EventModel.get_event')
    @patch('objects.ticket_checker.TicketModel.get_tickets_by_ticket_type')
    @patch('objects.ticket_checker.TicketTypeModel.get_ticket_type')
    def test_is_oversold_when_event_is_oversold(self, mock_get_ticket_type, mock_get_tickets_by_ticket_type, mock_get_event, mock_get_tickets_by_event):
        # mock
        mock_get_tickets_by_event.return_value = [
            {"id": "1"},
            {"id": "2"}
        ]
        mock_get_event.return_value = {"capacity": "1"}
        mock_get_tickets_by_ticket_type.return_value = [
            {"id": "1"},
            {"id": "2"}
        ]
        mock_get_ticket_type.return_value = {"limit": "100"}

        # testing
        ticket = Ticket({"event_id": "123", "ticket_type_id": "123"})
        assert TicketChecker(ticket).is_oversold()

    @patch('objects.ticket_checker.TicketModel.get_tickets_by_event')
    @patch('objects.ticket_checker.EventModel.get_event')
    @patch('objects.ticket_checker.TicketModel.get_tickets_by_ticket_type')
    @patch('objects.ticket_checker.TicketTypeModel.get_ticket_type')
    def test_is_oversold_when_ticket_type_is_oversold(self, mock_get_ticket_type, mock_get_tickets_by_ticket_type, mock_get_event, mock_get_tickets_by_event):
        # mock
        mock_get_tickets_by_event.return_value = [
            {"id": "1"},
            {"id": "2"}
        ]
        mock_get_event.return_value = {"capacity": "100"}
        mock_get_tickets_by_ticket_type.return_value = [
            {"id": "1"},
            {"id": "2"}
        ]
        mock_get_ticket_type.return_value = {"limit": "1"}

        # testing
        ticket = Ticket({"event_id": "123", "ticket_type_id": "123"})
        assert TicketChecker(ticket).is_oversold()

    @patch('objects.ticket_checker.TicketModel.get_tickets_by_event')
    @patch('objects.ticket_checker.EventModel.get_event')
    @patch('objects.ticket_checker.TicketModel.get_tickets_by_ticket_type')
    @patch('objects.ticket_checker.TicketTypeModel.get_ticket_type')
    def test_is_oversold_when_ticket_is_not_oversold(self, mock_get_ticket_type, mock_get_tickets_by_ticket_type, mock_get_event, mock_get_tickets_by_event):
        # mock
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

        #testing
        ticket = Ticket({"event_id": "123", "ticket_type_id": "123"})
        assert not TicketChecker(ticket).is_oversold()

    @patch('objects.ticket_checker.TicketModel.get_tickets_by_event')
    @patch('objects.ticket_checker.EventModel.get_event')
    @patch('objects.ticket_checker.TicketModel.get_tickets_by_ticket_type')
    @patch('objects.ticket_checker.TicketTypeModel.get_ticket_type')
    def test_is_oversold_when_event_and_ticket_type_do_not_exist(self, mock_get_ticket_type, mock_get_tickets_by_ticket_type, mock_get_event, mock_get_tickets_by_event):
        # mock
        mock_get_tickets_by_event.return_value = []
        mock_get_event.return_value = {}
        mock_get_tickets_by_ticket_type.return_value = []
        mock_get_ticket_type.return_value = {}

        # testing
        ticket = Ticket({"event_id": "123", "ticket_type_id": "123"})
        assert TicketChecker(ticket).is_oversold()
