import boto3
import json
import logging
from botocore.exceptions import ClientError
from flask import Flask, jsonify, Response 


app = Flask(__name__)

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

@app.route('/')
def hello():
    database = boto3.resource('dynamodb')
    table = database.Table('Users')
    
    response = table.scan()
    data = response['Items']
    logger.info(data)

    return Response(json.dumps(data), status=200)
