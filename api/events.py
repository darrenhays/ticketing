import json
from flask import Blueprint, Response, request
from models.event_model import EventModel
from models.session_model import SessionModel
from objects.bulk_refund_processor import BulkRefundProcessor
from security.events import is_users_event, event_has_no_tickets_sold
from security.sessions import is_valid_session

events_blueprint = Blueprint('events', __name__)


@events_blueprint.route('/events', methods=['POST'])
@is_valid_session
def create_event():
    session_id = request.headers.get('session_id')
    user_id = SessionModel().get_session(session_id).get('user_id')
    attributes = json.loads(request.data)
    attributes['user_id'] = user_id
    try:
        event_record = EventModel().create_event(attributes)
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=409)
    return Response(json.dumps(event_record), status=200)


@events_blueprint.route('/events/<event_id>', methods=['PATCH'])
@is_valid_session
@is_users_event
def update_event(event_id):
    updated_attributes = json.loads(request.data)
    try:
        event_record = EventModel().update_event(event_id, updated_attributes)
    except Exception as e:
        return Response(json.dumps({'error': str(e)}), status=409)
    return Response(json.dumps(event_record), status=200)


@events_blueprint.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    event_record = EventModel().get_event(event_id)
    return Response(json.dumps(event_record), status=200)


@events_blueprint.route('/events/<event_id>', methods=['DELETE'])
@is_valid_session
@is_users_event
def cancel_event(event_id):
    user_id = EventModel().get_event(event_id).get('user_id')
    process_record = BulkRefundProcessor().process_bulk_refund(user_id, event_id)
    return Response(json.dumps(process_record), status=200)
