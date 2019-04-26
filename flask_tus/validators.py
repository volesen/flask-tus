import hashlib

from flask import request, current_app

from .constants import SUPPORTED_ALGORITHMS
from .exceptions import TusError
from .utilities import extract_checksum, get_extension


def validate_version():
    # If the the version specified by the Client is not supported by the Server, it MUST respond with the 412
    # Precondition Failed status and MUST include the Tus-Version header into the response. In addition, the Server
    # MUST NOT process the request.
    if request.headers.get('Tus-Version') != '1.0.0':
        raise TusError(412)


# Link: https://tus.io/protocols/resumable-upload.html#patch
def validate_patch(upload):
    # If the servers receives a PATCH request against a non-existent resource it SHOULD return a 404 Not Found status.
    if upload is None:
        raise TusError(404)

    if upload.expired:
        raise TusError(410)

    # All PATCH requests MUST use Content-Type: application/offset+octet-stream, otherwise the server SHOULD return a
    #  415 Unsupported Media Type status.
    if request.headers.get('Content-Type') != 'application/offset+octet-stream':
        raise TusError(415)

    # The Upload-Offset header's value MUST be equal to the current offset of the resource. If the offsets do not
    # match, the Server MUST respond with the 409 Conflict status without modifying the upload resource.
    if int(request.headers.get('Upload-Offset')) != upload.offset:
        raise TusError(409)

    # If a PATCH request does not include a Content-Length header containing an integer value larger than 0,
    # the server SHOULD return a 400 Bad Request status.
    if int(request.headers.get('Content-Length')) <= 0:
        raise TusError(400)

    # If a PATCH request does not include a chunk, raise error
    if request.data is None:
        raise TusError(404)

    upload_checksum = request.headers.get('Upload-Checksum')
    if upload_checksum is not None:
        validate_chunk(request.data, upload_checksum)


# Link: https://tus.io/protocols/resumable-upload.html#checksum
def validate_chunk(chunk, upload_checksum):
    algorithm, checksum = extract_checksum(upload_checksum)

    # The server may respond 400 Bad Request if the checksum algorithm is not supported by the server
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise TusError(400)

    m = hashlib.new(algorithm)
    m.update(chunk)

    # The server may respond 460 Checksum Mismatch if the checksums mismatch
    if m.hexdigest() != checksum:
        raise TusError(460)


# Link: https://tus.io/protocols/resumable-upload.html#head
def validate_head(upload):
    # If the servers receives a HEAD request against a non-existent resource it SHOULD return a 404 Not Found status.
    if upload is None:
        raise TusError(404)


def validate_post():
    # If the length of the upload exceeds the maximum, which MAY be specified using the Tus-Max-Size header, 
    # the Server MUST respond with the 413 Request Entity Too Large status.
    upload_length = request.headers.get('Upload_Length')

    if upload_length is None:
        return

    if int(upload_length) > current_app.config['TUS_MAX_SIZE']:
        raise TusError(413)


def validate_delete(upload):
    # If the servers receives a HEAD request against a non-existent resource it SHOULD return a 404 Not Found status.
    if upload is None:
        raise TusError(404)

    # Check if termination-extension is used
    if 'termination' not in current_app.config['TUS_EXTENSION']:
        raise TusError(404)


def validate_metadata(metadata):
    # Check if extension is allowed
    filename = metadata.get('filename')

    # If filename or extension rules are not set
    if not filename or not current_app.config.get('TUS_EXTENSION_WHITELIST') or not current_app.config.get('TUS_EXTENSION_BLACKLIST'):
        return

    if current_app.config.get('TUS_EXTENSION_WHITELIST'):
        if get_extension(filename) not in current_app.config.get('TUS_EXTENSION_WHITELIST'):
            raise TusError(406, 'Extensions not allowed')
    else:
        if get_extension(filename) in current_app.config.get('TUS_EXTENSION_BLACKLIST'):
            raise TusError(406, 'Extensions not allowed')
