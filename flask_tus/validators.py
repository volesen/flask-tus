from flask import request, abort


def validate_patch(offset):
    if request.headers['Content-Type'] != 'application/offset+octet-stream':
        abort(415)

    if int(request.headers['Upload-Offset']) != int(offset):
        abort(409)

    if not int(request.headers['Content-Length']) > 0:
        abort(400)
