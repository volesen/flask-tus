from flask_tus.responses import make_base_response


class TusError(Exception):
    status_code = None

    def __init__(self, status_code):
        Exception.__init__(self)
        self.status_code = status_code

    @staticmethod
    def error_handler(error):
        response = make_base_response(error.status_code)
        response.status_code = error.status_code

        return response
