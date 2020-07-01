import json
import logging
from datetime import datetime
from flask import request, Response
from functools import wraps
from models.session_model import SessionModel

logger = logging.getLogger()


def is_authenticated(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        session_id = request.headers.get('session_id')
        session_record = SessionModel().get_session(session_id)
        expiration = datetime.strptime(session_record.get('expiration'), '%Y-%m-%d %H:%M:%S.%f')
        try:
            if datetime.now() <= expiration: 
                return f(*args, **kwargs)
        except:
            pass
        return Response(json.dumps({'message': 'unable to authenticate'}), status=403)
    return wrapped
