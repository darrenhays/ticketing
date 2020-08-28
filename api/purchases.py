import json
import logging
from flask import Blueprint, Response, request
from models.purchase_model import PurchaseModel
from models.ticket_model import TicketModel
from objects.payment_handler import PaymentHandler
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
            return Response(json.dumps({"message": "one or more items are no longer available"}), status=400)
    grand_total = 0
    for ticket in created_tickets:
        grand_total += float(ticket.get('amount_paid'))
    payment_credentials = attributes.get('payment_credentials')
    payment_completed = PaymentHandler().process_payment(payment_credentials, grand_total)  # process payment here
    if payment_completed:
        purchase_attributes = {
            "user_id": user_id,
            "total": str(grand_total),
            "purchased_items": created_tickets
        }
        purchase_record = PurchaseModel().create_purchase(purchase_attributes)
        return Response(json.dumps(purchase_record), status=200)
    else:
        return Response(json.dumps({'message': 'payment error'}), status=402)


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
    item_ids_to_refund = json.loads(request.data)
    purchase_record = PurchaseModel().get_purchase(purchase_id)
    updated_purchase_record = {}
    updated_purchase_record['purchased_items'] = purchase_record.get('purchased_items', [])
    updated_purchase_record['refunded_items'] = purchase_record.get('refunded_items', [])
    refund_total = 0.0
    refunded_ticket_ids = []
    for item_id_to_refund in item_ids_to_refund:
        for i, purchased_item in enumerate(updated_purchase_record['purchased_items']):
            if item_id_to_refund == purchased_item.get('id'):
                refund_total += float(purchased_item.get('amount_paid'))
                updated_purchase_record['refunded_items'].append(updated_purchase_record['purchased_items'].pop(i))
                refunded_ticket_ids.append(item_id_to_refund)
                break
        else:
            return Response(json.dumps({"message": "one or more items are not available for refund"}), status=400)
    purchase_record = PurchaseModel().update_purchase(purchase_id, updated_purchase_record)
    if purchase_record:
        if PaymentHandler().process_refund(refund_total):
            for ticket_to_delete in refunded_ticket_ids:
                TicketModel().delete_ticket(ticket_to_delete)
            return Response(json.dumps(purchase_record), status=200)
    return Response(json.dumps({"message": "could not process refund"}), status=400)
