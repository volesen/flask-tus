from flask_tus.responses import make_base_response


class TusError(Exception):
    def __init__(self, status_code):
        Exception.__init__(self)
        self.status_code = status_code


def handle_tus_error(error):
    response = make_base_response(error.status_code)
    response.status_code = error.status_code
    return response
