import json
import logging

import flask
from flask import Flask
from flask import request, jsonify

from api.handler import PredictionHandler


def return_500_if_errors(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.exception(e)
            response = {
                'error': True,
                'status_code': 500,
                'msg': str(e)
            }
            return flask.jsonify(response), 500

    return wrapper


def create_restyolo_api(opt):
    app = Flask(__name__)
    handler = PredictionHandler(opt)

    @app.route('/detect', methods=["POST"])
    @return_500_if_errors
    def detect():
        request_data = request.json
        logging.info(f"Predicting {', '.join(request_data.keys())}")
        response = handler.predict(request_data)
        logging.info(json.dumps(response, indent=4, sort_keys=True))
        return jsonify(response)

    return app
