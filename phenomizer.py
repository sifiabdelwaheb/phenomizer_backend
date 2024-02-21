from flask import Flask, has_request_context, request
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from ma import ma
import logging

from resources.Phenomizer import Phenomizer

app = Flask(__name__)


# using custom formatter to inject contextual data into logging
class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)


formatter = RequestFormatter(
    "[%(asctime)s] %(remote_addr)s requested %(url)s\n"
    "%(levelname)s in %(module)s: %(message)s"
)

logger = logging.getLogger()
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)


CORS(app, supports_credentials=True)
app.config["PROPAGATE_EXCEPTIONS"] = True
# Setup the Flask-JWT-Extended extension
app.secret_key = "sifi"  ## Change JWT secret key optionals
api = Api(app)
jwt = JWTManager(app)
# mail = Mail(app)


api.add_resource(Phenomizer, "/phenomizer")


# api.add_resource(ImageUpload, '/image')


@app.route("/")
def helloword():
    app.logger.error("API request received: /")
    return "api tets"


if __name__ == "__main__":
    ma.init_app(app)
    app.run(host="0.0.0.0", debug=True)
