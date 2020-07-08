import logging
from api.sessions import sessions_blueprint
from api.users import users_blueprint
from flask import Flask, Response, request

app = Flask(__name__)
app.register_blueprint(sessions_blueprint)
app.register_blueprint(users_blueprint)

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


#FIXME write a readme file for running the system locally

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
