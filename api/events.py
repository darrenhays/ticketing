import json
from flask import Blueprint, Response, request
from models.event_model import EventModel
from models.session_model import SessionModel
from security.sessions import is_valid_session

events_blueprint = Blueprint('events', __name__)


@events_blueprint.route('/events', methods=['POST'])
@is_valid_session
def create_event():
    session_id = request.headers.get('session_id')
    attributes = json.loads(request.data)
    user_id = SessionModel().get_session(session_id).get('user_id')
    attributes['user_id'] = user_id
    try:
        event_record = EventModel().create_event(attributes)
    except Exception as e:
        return Response(json.dumps({'message': str(e)}), status=409)
    return Response(json.dumps(event_record), status=200)


@events_blueprint.route('/events/<event_id>', methods=['PATCH'])
@is_valid_session
def update_event(event_id):
    updated_attributes = json.loads(request.data)
    try:
        event_record = EventModel().update_event(event_id, updated_attributes)
    except Exception as e:
        return Response(json.dumps({'message': str(e)}), status=409)
    return Response(json.dumps(event_record), status=200)


@events_blueprint.route('/events/<event_id>', methods=['GET'])
@is_valid_session
def get_events(event_id):
    event_record = EventModel().get_event(event_id)
    return Response(json.dumps(event_record), status=200)


@events_blueprint.route('/events/<event_id>', methods=['DELETE'])
@is_valid_session
def delete_event(event_id):
    if EventModel().delete_event(event_id):
        response = {'message': 'success'}
    else:
        response = {'message': 'failure'}
    return Response(json.dumps(response), status=200)
