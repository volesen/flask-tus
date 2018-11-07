from flask import make_response, current_app


def make_base_response(status_code):
    # If this was inherited from flask.Response changing the response_class for the app object (eg. for custom
    # headers or CSRF tokens), would not affect TUS-responses, thus this pattern
    response = make_response('', status_code)
    response.headers['Tus-Resumable'] = '1.0.0'
    response.headers['Tus-Version'] = '1.0.0'
    response.headers['Tus-Max-Size'] = current_app.config['TUS_MAX_SIZE']
    return response


def post_response(upload):
    # The Server MUST acknowledge a successful upload creation with the 201 Created status.
    response = make_base_response(201)

    # The Upload-Defer-Length response header indicates that the size of the upload is not known currently and will
    # be transferred later. Its value MUST be 1. If the length of an upload is not deferred, this header MUST be
    # omitted.
    if upload.length is None:
        response.headers['Upload-Defer-Length'] = '1'
    else:
        response.headers['Upload-Length'] = upload.length

    # The Server MUST set the Location header to the URL of the created resource. This URL MAY be absolute or relative.
    response.headers['location'] = current_app.config['TUS_UPLOAD_URL'] + upload.upload_id

    return response


def head_response(upload):
    response = make_base_response(204)

    # The Server MUST always include the Upload-Offset header in the response for a HEAD request, even if the offset
    # is 0, or the upload is already considered completed.
    response.headers['Upload-Offset'] = upload.offset

    # If the size of the upload is known, the Server MUST include the Upload-Length header in the response.
    if upload.length is None:
        response.headers['Upload-Defer-Length'] = '1'
    else:
        response.headers['Upload-Length'] = upload.length

    # The Server MUST prevent the client and/or proxies from
    # caching the response by adding the Cache-Control: no-store
    # header to the response
    response.headers['Cache-Control'] = 'no-store'

    return response


def patch_response(upload):
    response = make_base_response(204)
    # The Server MUST acknowledge successful PATCH requests with the 204 No Content status. It MUST include the
    # Upload-Offset header containing the new offset.
    response.headers['Upload-Offset'] = upload.offset

    return response


def option_response():
    # A successful response indicated by the 204 No Content or 200 OK status MUST contain the Tus-Version header.
    response = make_base_response(204)

    # It MAY include the Tus-Extension and Tus-Max-Size headers.
    response.headers['Tus-Extensions'] = 'creation'

    return response
