import json
from flask import Blueprint, Response, request
from models.session_model import SessionModel
from models.user_model import UserModel
from objects.password import Password
from security.sessions import is_valid_session

sessions_blueprint = Blueprint('sessions', __name__)


@sessions_blueprint.route('/sessions', methods=['POST'])
def create_session():
    request_data = json.loads(request.data)
    email = request_data.get('email')
    password = request_data.get('password')
    user_record = UserModel().get_user_by_email(email)
    if user_record.get('password') == Password(password):
        session_record = SessionModel().create_session(user_record.get('id'))
        return Response(json.dumps({'session_id': session_record.get('id')}), status=200)
    else:
        return Response(json.dumps({'message': 'invalid credentials'}), status=403)


@sessions_blueprint.route('/sessions/<session_id>', methods=['DELETE'])
@is_valid_session
def delete_session(session_id):
    SessionModel().delete_session(session_id)
    return Response(json.dumps({'message': 'success'}), status=200)
