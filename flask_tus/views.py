from tempfile import mkdtemp

from flask import request

from flask_tus.exceptions import TusError, handle_request_error
from flask_tus.models import TusUploads
from flask_tus.responses import head_response, option_response, post_response, patch_response
from flask_tus.validators import validate_patch


class FlaskTus(object):
    uploads = None

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('TUS_UPLOAD_DIR', mkdtemp())
        app.config.setdefault('TUS_UPLOAD_URL', '/files/')

        self.uploads = TusUploads(app.config['TUS_UPLOAD_DIR'])
        app.register_error_handler(TusError, handle_request_error)

        app.add_url_rule(app.config['TUS_UPLOAD_URL'], 'create_upload_resource', self.create_upload_resource,
                         methods=['OPTIONS', 'POST'])
        app.add_url_rule('{}<upload_id>'.format(app.config['TUS_UPLOAD_URL']), 'upload_resource',
                         self.upload_resource,
                         methods=['HEAD', 'PATCH'])

    def create_upload_resource(self):
        if request.method == 'OPTIONS':
            return option_response()

        upload_length = request.headers.get('Upload-Length')
        upload = self.uploads.create_upload(upload_length)

        return post_response(upload)

    def upload_resource(self, upload_id):
        upload = self.uploads.get_upload_or_404(upload_id)
        if request.method == 'HEAD':
            # validate_head()
            return head_response(upload)

        validate_patch(upload)

        chunk = request.data
        if chunk is None:
            raise TusError(404)
        upload.append_chunk(chunk)
        return patch_response(upload)
