from flask import request

from flask_tus.responses import make_base_response


class RequestError(Exception):
    def __init__(self, status_code):
        Exception.__init__(self)
        self.status_code = status_code


def handle_request_error(error):
    response = make_base_response()
    response.status_code = error.status_code
    return response


def validate_version():
    # If the the version specified by the Client is not supported by the Server, it MUST respond with the 412
    # Precondition Failed status and MUST include the Tus-Version header into the response. In addition, the Server
    # MUST NOT process the request.
    if request.headers.get('Tus-Version') != '1.0.0':
        raise RequestError(412)


def validate_patch(upload):
    # All PATCH requests MUST use Content-Type: application/offset+octet-stream, otherwise the server SHOULD return a
    #  415 Unsupported Media Type status.
    if request.headers.get('Content-Type') != 'application/offset+octet-stream':
        raise RequestError(415)

    # The Upload-Offset header’s value MUST be equal to the current offset of the resource.  If the offsets do not
    # match, the Server MUST respond with the 409 Conflict status without modifying the upload resource.
    if int(request.headers.get('Upload-Offset')) != upload.offset:
        raise RequestError(409)

    # If a PATCH request does not include a Content-Length header containing an integer value larger than 0,
    # the server SHOULD return a 400 Bad Request status.
    if not int(request.headers.get('Content-Length')) > 0:
        raise RequestError(400)
