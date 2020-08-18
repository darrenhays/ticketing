import datetime
import json
import logging
from flask import Blueprint, Response, request
from models.purchase_model import PurchaseModel
from models.ticket_model import TicketModel
from objects.payment_handler import PaymentHandler
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
        if TicketChecker(requested_ticket_record).is_oversold():
            for item in created_tickets:
                TicketModel().delete_ticket(item.get('id'))
            return Response(json.dumps({"message": "one or more items are no longer available"}), status=400)
    grand_total = 0
    for ticket in created_tickets:
        grand_total += float(ticket.get('price'))
    payment_credentials = attributes.get('payment_credentials')
    payment_completed = PaymentHandler().process_payment(payment_credentials, grand_total)  # process payment here
    if payment_completed:
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        purchase_attributes = {
            "user_id": user_id,
            "timestamp": timestamp,
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


@purchases_blueprint.route('/purchases/<purchase_id>/refund', methods=['DELETE'])
@is_valid_session
@is_users_purchase
def refund_items(purchase_id):
    attributes = json.loads(request.data)
    purchase_record = PurchaseModel().get_purchase(purchase_id)
    purchased_items = purchase_record.get('purchased_items')
    refunded_items = []
    for item_to_refund in attributes:
        for i, purchased_item in enumerate(purchased_items):
            if item_to_refund.get('item_id') == purchased_item.get('id'):
                refunded_items.append(purchased_items.pop(i))
                break
        else:
            return Response(json.dumps({"message": "one or more items are not available for refund"}), status=400)
    purchase_record['purchased_items'] = purchased_items
    purchase_record['refunded_items'] = refunded_items
    purchase_record.pop('id')
    purchase_record = PurchaseModel().update_purchase(purchase_id, purchase_record)
    return Response(json.dumps(purchase_record), status=200)
