import logging
from models.purchase_model import PurchaseModel
from models.ticket_model import TicketModel
from objects.payment_handler import PaymentHandler
from objects.ticket import Ticket
from objects.ticket_checker import TicketChecker
from objects.ticket_processor import TicketProcessor

logger = logging.getLogger()


class ItemsNotAvailable(Exception):
    pass


class PaymentError(Exception):
    pass


class PurchaseProcessor():
    def process_purchase(self, user_id, requested_tickets, payment_token):
        logger.info("########## {} process_purchase ##########".format(self.__class__.__name__))
        logger.info("user_id: {}".format(user_id))
        logger.info("requested_tickets: {}".format(requested_tickets))
        logger.info("payment_token: {}".format(payment_token))
        created_tickets = []
        for requested_ticket_record in requested_tickets:
            created_tickets.extend(TicketProcessor().process_record(requested_ticket_record))
            if TicketChecker(Ticket(requested_ticket_record)).is_oversold():
                for item in created_tickets:
                    TicketModel().delete_ticket(item.get('id'))
                logger.error("########## {} process_purchase: failure ##########".format(self.__class__.__name__))
                logger.error("########## one or more items not available ##########")
                raise ItemsNotAvailable('one or more items not available')
        grand_total = 0
        for ticket in created_tickets:
            grand_total += float(ticket.get('amount_paid'))
        payment_completed = PaymentHandler().process_payment(payment_token, grand_total)
        if not payment_completed:
            for ticket in created_tickets:
                TicketModel().delete_ticket(ticket.get('id'))
            logger.error("########## {} process_purchase: failure ##########".format(self.__class__.__name__))
            logger.error("########## payment error ##########")
            raise PaymentError('payment error')
        else:
            purchase_attributes = {
                "user_id": user_id,
                "total": str(grand_total),
                "purchased_items": created_tickets,
                "payment_id": payment_completed.get('id')
            }
            purchase_record = PurchaseModel().create_purchase(purchase_attributes)
            for ticket in created_tickets:
                updated_attributes = {"purchase_id": purchase_record.get('id')}
                TicketModel().update_ticket(ticket.get('id'), updated_attributes)
            logger.error("########## {} process_purchase: success ##########".format(self.__class__.__name__))
            return purchase_record
