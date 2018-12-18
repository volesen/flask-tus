from flask import jsonify
from flask_tus.responses import make_base_response


class TusError(Exception):
    status_code = 500
    throw_as = 'Header'

    def __init__(self, status_code=500, message='', throw_as='Header'):
        Exception.__init__(self, message)
        self.throw_as = throw_as
        self.message = message
        self.status_code = status_code

    @staticmethod
    def error_handler(error):

        if error.throw_as == 'Exception':
            raise error

        if error.throw_as == 'Header':
            response = make_base_response(error.status_code)
            response.message = error.message
            response.status_code = error.status_code

            return response

        if error.throw_as == 'JSON':
            return jsonify(status_code=error.status_code, data={'error': error.message, 'success': False})
