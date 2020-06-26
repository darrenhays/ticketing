import json
import logging
from flask import Flask, Response, request 
from models.user_model import UserModel
from objects.user import User

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route('/users', methods=['POST'])
def create_user():
    request_data = json.loads(request.data)
    email = request_data['email']
    password = request_data['password']
    user = UserModel().create_user(email=email, password=password)
    return Response(user.jsonify(), status=200, mimetype='application/json')

@app.route('/users', methods=['PATCH'])
def update_user():
    request_data = json.loads(request.data)
    id = request_data['id']
    email = request_data['email']
    password = request_data['password']
    user = UserModel().update_user(User(id=id, email=email, password=password))
    return Response(user.jsonify(), status=200, mimetype='application/json')

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = UserModel().get_user(user_id)
    return Response(user.jsonify(), status=200, mimetype='application/json')

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if UserModel().delete(user_id):
        response = {'message': 'success'}
    else:
        response = {'message': 'failure'}
    return Response(json.dumps(response), status=200, mimetype='application/json')
