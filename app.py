import json
import logging
from flask import Flask, Response, request 
from models.user_model import UserModel

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
    logger.info(user)
    return Response(user.jsonify(), status=200, mimetype='application/json')

@app.route('/users', methods=['GET'])
def get_user():
    id = request.args.get("id")
    user = UserModel().get_user(id)
    logger.info(user)
    return Response(user.jsonify(), status=200, mimetype='application/json')
