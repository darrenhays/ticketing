import json
from flask import Blueprint, Response, request
from models.user_model import UserModel
from objects.user import User
from security.sessions import is_valid_session, user_is_session_user

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users', methods=['POST'])
def create_user():
    attributes = json.loads(request.data)
    try:
        user_record = UserModel().create_user(attributes)
    except Exception as e:
        return Response(json.dumps({'message': str(e)}), status=400) #FIXME status code
    user = User(user_record)
    return Response(user.jsonify(), status=200)


@users_blueprint.route('/users/<user_id>', methods=['PATCH'])
@is_valid_session
@user_is_session_user
def update_user(user_id):
    updated_attributes = json.loads(request.data)
    try:
        user_record = UserModel().update_user(user_id, updated_attributes)
    except Exception as e:
        return Response(json.dumps({'message': str(e)}), status=400) #FIXME status code
    user = User(user_record)
    return Response(user.jsonify(), status=200)


@users_blueprint.route('/users/<user_id>', methods=['GET'])
@is_valid_session
@user_is_session_user
def get_user(user_id):
    user_record = UserModel().get_user(user_id)
    user = User(user_record)
    return Response(user.jsonify(), status=200)


@users_blueprint.route('/users/<user_id>', methods=['DELETE'])
@is_valid_session
@user_is_session_user
def delete_user(user_id):
    if UserModel().delete_user(user_id):
        response = {'message': 'success'}
    else:
        response = {'message': 'failure'}
    return Response(json.dumps(response), status=200)
