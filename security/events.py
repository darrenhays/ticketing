import json
import logging
from flask import request, Response
from functools import wraps
from models.event_model import EventModel
from models.session_model import SessionModel
from models.ticket_type_model import TicketTypeModel

logger = logging.getLogger()


def is_users_event(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        session_id = request.headers.get('session_id')
        event_id = kwargs.get('event_id')
        user_id = SessionModel().get_session(session_id).get('user_id')
        event_user_id = EventModel().get_event(event_id).get('user_id')
        if user_id == event_user_id:
            return f(*args, **kwargs)
        else:
            return Response(json.dumps({'message': 'unauthorized'}), status=403)
    return wrapped


def is_events_ticket_type(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        event_id = kwargs.get('event_id')
        ticket_type_id = kwargs.get('ticket_type_id')
        ticket_type_event_id = TicketTypeModel().get_ticket_type(ticket_type_id).get('event_id')
        if event_id == ticket_type_event_id:
            return f(*args, **kwargs)
        else:
            return Response(json.dumps({'message': 'unauthorized'}), status=403)
    return wrapped
