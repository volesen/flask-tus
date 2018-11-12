from tempfile import mkdtemp

from flask import request, current_app

from flask_tus.exceptions import TusError, handle_tus_error
from flask_tus.ext.memory_upload import MemoryUpload
from flask_tus.responses import head_response, option_response, post_response, patch_response
from flask_tus.validators import validate_patch


class FlaskTus(object):
    def __init__(self, app=None, model=MemoryUpload):
        self.app = app
        if app is not None:
            self.init_app(app, model)

    def init_app(self, app, model=MemoryUpload):
        app.config.setdefault('TUS_UPLOAD_DIR', mkdtemp())
        app.config.setdefault('TUS_UPLOAD_URL', '/files/')
        app.model = model(app.config['TUS_UPLOAD_DIR'])
        app.register_error_handler(TusError, handle_tus_error)
        app.add_url_rule(app.config['TUS_UPLOAD_URL'], 'create_upload_resource', self.create_upload_resource,
                         methods=['OPTIONS', 'POST'])
        app.add_url_rule('{}<upload_id>'.format(app.config['TUS_UPLOAD_URL']), 'upload_resource',
                         self.upload_resource,
                         methods=['HEAD', 'PATCH'])

    def create_upload_resource(self):
        if request.method == 'OPTIONS':
            return option_response()

        upload_length = request.headers.get('Upload-Length')
        upload = current_app.model.create(upload_length)

        return post_response(upload)

    def upload_resource(self, upload_id):
        upload = current_app.model.get(upload_id)
        if upload is None:
            raise TusError(404)

        if request.method == 'HEAD':
            # validate_head()
            return head_response(upload)

        validate_patch(upload)

        chunk = request.data
        if chunk is None:
            raise TusError(404)

        upload.append_chunk(chunk)
        return patch_response(upload)
