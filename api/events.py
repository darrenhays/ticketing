import json
from flask import Blueprint, Response, request
from models.event_model import EventModel
from models.session_model import SessionModel
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
        return Response(json.dumps({'message': str(e)}), status=409)
    return Response(json.dumps(event_record), status=200)


@events_blueprint.route('/events/<event_id>', methods=['PATCH'])
@is_valid_session
@is_users_event
def update_event(event_id):
    updated_attributes = json.loads(request.data)
    try:
        event_record = EventModel().update_event(event_id, updated_attributes)
    except Exception as e:
        return Response(json.dumps({'message': str(e)}), status=409)
    return Response(json.dumps(event_record), status=200)


@events_blueprint.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    event_record = EventModel().get_event(event_id)
    return Response(json.dumps(event_record), status=200)


@events_blueprint.route('/events/<event_id>', methods=['DELETE'])
@event_has_no_tickets_sold
@is_valid_session
@is_users_event
def delete_event(event_id):
    if EventModel().delete_event(event_id):
        return Response(json.dumps({'message': 'success'}), status=200)
    else:
        return Response(json.dumps({'message': 'failure'}), status=409)
