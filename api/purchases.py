import json
import logging
from flask import Blueprint, Response, request
from models.purchase_model import PurchaseModel
from models.ticket_model import TicketModel
from objects.payment_handler import PaymentHandler
from objects.refund_processor import RefundProcessor
from objects.ticket import Ticket
from objects.ticket_checker import TicketChecker
from objects.ticket_processor import TicketProcessor
from security.purchases import is_users_purchase
from security.sessions import is_valid_session

purchases_blueprint = Blueprint('purchases', __name__)
logger = logging.getLogger()


@purchases_blueprint.route('/purchases', methods=['POST'])
def create_purchase():
    attributes = json.loads(request.data)
    user_id = attributes.get('user_id')
    requested_tickets = attributes.get('items')
    created_tickets = []
    for requested_ticket_record in requested_tickets:
        created_tickets.extend(TicketProcessor().process_record(requested_ticket_record))
        if TicketChecker(Ticket(requested_ticket_record)).is_oversold():
            for item in created_tickets:
                TicketModel().delete_ticket(item.get('id'))
            return Response(json.dumps({"error": "one or more items are no longer available"}), status=400)
    grand_total = 0
    for ticket in created_tickets:
        grand_total += float(ticket.get('amount_paid'))
    payment_token = attributes.get('payment_token')
    payment_completed = PaymentHandler().process_payment(payment_token, grand_total)
    if not payment_completed:
        for ticket in created_tickets:
            TicketModel().delete_ticket(ticket.get('id'))
        return Response(json.dumps({'error': 'payment error'}), status=402)
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
        return Response(json.dumps(purchase_record), status=200)


@purchases_blueprint.route('/purchases/<purchase_id>', methods=['GET'])
@is_valid_session
@is_users_purchase
def get_purchase(purchase_id):
    purchase_record = PurchaseModel().get_purchase(purchase_id)
    return Response(json.dumps(purchase_record), status=200)


@purchases_blueprint.route('/purchases/<purchase_id>/refund', methods=['POST'])
@is_valid_session
@is_users_purchase
def refund_items(purchase_id):
    item_ids = json.loads(request.data)
    response = RefundProcessor().process_refund(purchase_id, item_ids)
    if response.get('error'):
        return Response(json.dumps(response), status=400)
    return Response(json.dumps(response), status=200)


