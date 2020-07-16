import json
import logging
from api.events import events_blueprint
from api.sessions import sessions_blueprint
from api.ticket_types import ticket_types_blueprint
from api.users import users_blueprint
from flask import Flask, Response, request

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.register_blueprint(events_blueprint)
app.register_blueprint(sessions_blueprint)
app.register_blueprint(ticket_types_blueprint)
app.register_blueprint(users_blueprint)


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


@app.route('/', methods=['GET'])
def index():
    return Response(json.dumps({'message': 'success'}), status=200)
