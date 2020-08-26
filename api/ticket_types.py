import json
from flask import Blueprint, Response, request
from models.ticket_type_model import TicketTypeModel
from security.events import is_users_event, is_events_ticket_type, ticket_type_has_no_tickets_sold
from security.sessions import is_valid_session

ticket_types_blueprint = Blueprint('ticket_types', __name__)


@ticket_types_blueprint.route('/events/<event_id>/ticket-types', methods=['POST'])
@is_valid_session
@is_users_event
def create_ticket_type(event_id):
    attributes = json.loads(request.data)
    try:
        ticket_type_record = TicketTypeModel().create_ticket_type(attributes)
    except Exception as e:
        return Response(json.dumps({'message': str(e)}), status=409)
    return Response(json.dumps(ticket_type_record), status=200)


@ticket_types_blueprint.route('/events/<event_id>/ticket-types/<ticket_type_id>', methods=['PATCH'])
@is_valid_session
@is_users_event
@is_events_ticket_type
def update_ticket_type(event_id, ticket_type_id):
    updated_attributes = json.loads(request.data)
    try:
        ticket_type_record = TicketTypeModel().update_ticket_type(ticket_type_id, updated_attributes)
    except Exception as e:
        return Response(json.dumps({'message': str(e)}), status=409)
    return Response(json.dumps(ticket_type_record), status=200)


@ticket_types_blueprint.route('/events/<event_id>/ticket-types/<ticket_type_id>', methods=['GET'])
def get_ticket_type(event_id, ticket_type_id):
    ticket_type_record = TicketTypeModel().get_ticket_type(ticket_type_id)
    return Response(json.dumps(ticket_type_record), status=200)


@ticket_types_blueprint.route('/events/<event_id>/ticket-types/<ticket_type_id>', methods=['DELETE'])
@ticket_type_has_no_tickets_sold
@is_valid_session
@is_users_event
@is_events_ticket_type
def delete_ticket_type(event_id, ticket_type_id):
    if TicketTypeModel().delete_ticket_type(ticket_type_id):
        return Response(json.dumps({'message': 'success'}), status=200)
    else:
        return Response(json.dumps({'message': 'failure'}), status=409)
