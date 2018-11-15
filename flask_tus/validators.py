from flask import request
from flask_tus.exceptions import TusError


def validate_version():
    # If the the version specified by the Client is not supported by the Server, it MUST respond with the 412
    # Precondition Failed status and MUST include the Tus-Version header into the response. In addition, the Server
    # MUST NOT process the request.
    if request.headers.get('Tus-Version') != '1.0.0':
        raise TusError(412)


# link: https://tus.io/protocols/resumable-upload.html#patch
def validate_patch(upload):
    # All PATCH requests MUST use Content-Type: application/offset+octet-stream, otherwise the server SHOULD return a
    #  415 Unsupported Media Type status.
    if request.headers.get('Content-Type') != 'application/offset+octet-stream':
        raise TusError(415)

    # The Upload-Offset header’s value MUST be equal to the current offset of the resource.  If the offsets do not
    # match, the Server MUST respond with the 409 Conflict status without modifying the upload resource.
    if int(request.headers.get('Upload-Offset')) != upload.offset:
        raise TusError(409)

    # If a PATCH request does not include a Content-Length header containing an integer value larger than 0,
    # the server SHOULD return a 400 Bad Request status.
    if int(request.headers.get('Content-Length')) <= 0:
        raise TusError(400)

    # TODO: Implement 404 -If the servers receives a PATCH request against a non-existent resource it SHOULD return a 404 Not Found status.


# TODO: validate head request/response
# link: https://tus.io/protocols/resumable-upload.html#head
def validate_head(upload):
    pass
