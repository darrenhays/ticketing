import json
import logging
from flask import request, Response
from functools import wraps
from models.purchase_model import PurchaseModel
from models.session_model import SessionModel

logger = logging.getLogger()


def is_users_purchase(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        logger.info("########## is_users_purchase ##########")
        session_id = request.headers.get('session_id')
        user_id = SessionModel().get_session(session_id).get('user_id')
        purchase_id = kwargs.get('purchase_id')
        purchase_user_id = PurchaseModel().get_purchase(purchase_id).get('user_id')
        if user_id == purchase_user_id:
            logger.info("########## is_users_purchase: success ##########")
            return f(*args, **kwargs)
        else:
            logger.info("########## is_users_purchase: failure ##########")
            return Response(json.dumps({'message': 'unauthorized'}), status=403)
    return wrapped
