import json
import logging
from flask import Flask, Response, request
from models.session_model import SessionModel
from models.user_model import UserModel
from objects.password import Password
from objects.user import User
from security.sessions import is_valid_session, user_is_session_user

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def before_request_handler():
    logger.debug('########## Request Received ########################################')
    logger.debug({'method': request.method})
    logger.debug({'url': request.url})
    logger.debug({'headers': request.headers})
    logger.debug({'body': request.data})
app.before_request(before_request_handler)

def after_request_handler(response):
    response.headers = {"Content-Type": "application/json"}
    logger.debug('########## Response Sent ########################################')
    logger.debug({'status': response.status})
    logger.debug({'headers': response.headers})
    logger.debug({'body': response.response})
    return response
app.after_request(after_request_handler)

@app.route('/sessions', methods=['POST'])
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

@app.route('/users', methods=['POST'])
def create_user():
    attributes = json.loads(request.data)
    try:
        user_record = UserModel().create_user(attributes)
    except Exception as e:
        return Response(json.dumps({'message': str(e)}), status=400) #FIXME status code
    user = User(user_record)
    return Response(user.jsonify(), status=200)

@app.route('/users/<user_id>', methods=['PATCH'])
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

@app.route('/users/<user_id>', methods=['GET'])
@is_valid_session
@user_is_session_user
def get_user(user_id):
    user_record = UserModel().get_user(user_id)
    user = User(user_record)
    return Response(user.jsonify(), status=200)

@app.route('/users/<user_id>', methods=['DELETE'])
@is_valid_session
@user_is_session_user
def delete_user(user_id):
    if UserModel().delete_user(user_id):
        response = {'message': 'success'}
    else:
        response = {'message': 'failure'}
    return Response(json.dumps(response), status=200)
