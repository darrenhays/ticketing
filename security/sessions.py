import json
import logging
from flask import request, Response
from functools import wraps
from models.session_model import SessionModel

logger = logging.getLogger()


def is_valid_session(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        logger.info("########## is_valid_session ##########")
        session_id = request.headers.get('session_id')
        if not session_id:
            logger.info("########## is_valid_session: no session_id")
            return Response(json.dumps({'message': 'unable to authenticate'}), status=401)
        session_record = SessionModel().get_session(session_id)
        if session_record:
            logger.info("########## is_valid_session: success")
            return f(*args, **kwargs)
        else:
            logger.info("########## is_valid_session: failure")
            return Response(json.dumps({'message': 'unable to authenticate'}), status=401)
    return wrapped


def user_is_session_user(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        logger.info("########## user_is_session_user ##########")
        session_user_id = request.headers.get('session_id')
        session = SessionModel().get_session(session_user_id)
        if kwargs.get('user_id') == session.get('user_id'):
            logger.info("########## user_is_session_user: success")
            return f(*args, **kwargs)
        logger.info("########## user_is_session_user: failure")
        return Response(json.dumps({'message': 'you do not have permission to access this resource'}), status=403)
    return wrapped
