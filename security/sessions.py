import json
import logging
from flask import request, Response
from functools import wraps
from models.session_model import SessionModel

logger = logging.getLogger()


def is_valid_session(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        session_id = request.headers.get('session_id')
        session_record = SessionModel().get_session(session_id)
        if session_record:
            return f(*args, **kwargs)
        else:
            return Response(json.dumps({'message': 'unable to authenticate'}), status=403)
    return wrapped


def user_is_session_user(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        session_id = request.headers.get('session_id')
        session = SessionModel().get_session(session_id)
        if kwargs.get('user_id') == session.get('user_id'):
            return f(*args, **kwargs)
        return Response(json.dumps({'message': 'you do not have permission to access this resource'}), status=403)
    return wrapped
