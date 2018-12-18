from flask_tus.responses import make_base_response
from flask import jsonify


class TusError(Exception):
    message = ''
    status_code = None

    def __init__(self, status_code, message=''):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    @staticmethod
    def error_handler(error):
        return jsonify(status_code=error.status_code, data={'error': error.message})
