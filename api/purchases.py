import json
import logging
from flask import Blueprint, Response, request
from models.purchase_model import PurchaseModel
from models.ticket_model import TicketModel
from objects.payment_handler import PaymentHandler
from objects.purchase_processor import PurchaseProcessor, ItemsNotAvailable, PaymentError
from objects.refund_processor import RefundProcessor, ItemsNotAvailable, ProcessingFailure
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
    payment_token = attributes.get('payment_token')
    try:
        response = PurchaseProcessor().process_purchase(user_id, requested_tickets, payment_token)
        return Response(json.dumps(response), status=200)
    except(ItemsNotAvailable, PaymentError) as e:
        return Response(json.dumps({'error': e}), status=400)


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
    try:
        response = RefundProcessor().process_refund(purchase_id, item_ids)
        return Response(json.dumps(response), status=200)
    except (ItemsNotAvailable, ProcessingFailure) as e:
        return Response(json.dumps({'error': e}), status=400)
