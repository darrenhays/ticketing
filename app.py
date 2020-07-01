import json
import logging
from flask import Flask, Response, request
from models.session_model import SessionModel
from models.user_model import UserModel
from objects.user import User
from security.sessions import is_authenticated

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
    if user_record.get('password') == password:
        session_record = SessionModel().create_session()
        return Response(json.dumps({'session_id': session_record.get('id')}), status=200)
    else:
        return Response(json.dumps({'message': 'invalid credentials'}), status=403)

@app.route('/users', methods=['POST'])
def create_user():
    request_data = json.loads(request.data)
    email = request_data.get('email')
    password = request_data.get('password')
    user_record = UserModel().get_user_by_email(email)
    if user_record:
        return Response(json.dumps({'message': 'email already exists'}), status=409)
    user_record = UserModel().create_user(email=email, password=password)
    user = User(user_record)
    return Response(user.jsonify(), status=200)

@app.route('/users/<user_id>', methods=['PATCH'])
@is_authenticated
def update_user(user_id):
    updated_attributes = json.loads(request.data)
    user_record = UserModel().update_user(user_id, updated_attributes)
    user = User(user_record)
    return Response(user.jsonify(), status=200)

@app.route('/users/<user_id>', methods=['GET'])
@is_authenticated
def get_user(user_id):
    user_record = UserModel().get_user(user_id)
    user = User(user_record)
    return Response(user.jsonify(), status=200)

@app.route('/users/<user_id>', methods=['DELETE'])
@is_authenticated
def delete_user(user_id):
    if UserModel().delete_user(user_id):
        response = {'message': 'success'}
    else:
        response = {'message': 'failure'}
    return Response(json.dumps(response), status=200)
