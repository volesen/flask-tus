from tempfile import mkdtemp
from flask import request
from flask_tus.exceptions import TusError
from flask_tus.models.memory_upload import MemoryUpload
from flask_tus.models.mongoengine_upload import MongoengineUpload
from flask_tus.helpers import handle_metadata
from flask_tus.responses import head_response, option_response, post_response, patch_response
from flask_tus.validators import validate_patch


class FlaskTus(object):
    app = None
    model = None

    def __init__(self, app=None, model=MemoryUpload):

        # TODO check for instanceof()
        # links: https://infohost.nmt.edu/tcc/help/pubs/python/web/isinstance-function.html
        # links: http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/
        # if str(model) == "flask_mongoengine.MongoEngine":
        #     model = MongoengineUpload

        self.app = app
        if app:
            self.init_app(app, model)

    # Application factory
    def init_app(self, app, model=MemoryUpload):
        app.config.setdefault('TUS_UPLOAD_DIR', mkdtemp())
        app.config.setdefault('TUS_UPLOAD_URL', '/files/')
        app.register_error_handler(TusError, TusError.error_handler)
        app.add_url_rule(app.config['TUS_UPLOAD_URL'], 'create_upload_resource', self.create_upload_resource, methods=['OPTIONS', 'POST'])
        app.add_url_rule('{}<upload_id>'.format(app.config['TUS_UPLOAD_URL']), 'upload_resource', self.upload_resource, methods=['HEAD', 'PATCH'])
        self.model = model

    def create_upload_resource(self):
        # Get server configuration
        if request.method == 'OPTIONS':
            return option_response()

        # Crate a resource
        if request.method == 'POST':
            upload_length = request.headers.get('Upload-Length')

            upload_metadata = request.headers.get('Upload-Metadata')
            if upload_metadata:
                upload_metadata = handle_metadata(upload_metadata)

            upload = self.model.create(upload_length, upload_metadata)

            return post_response(upload)

    def upload_resource(self, upload_id):
        upload = self.model.get(upload_id)
        if upload is None:
            raise TusError(404)

        # Get state of a resource
        if request.method == 'HEAD':
            # TODO validate_head()
            return head_response(upload)

        # Update a resource
        if request.method == 'PATCH':
            validate_patch(upload)

            chunk = request.data
            if chunk is None:
                raise TusError(404)

            upload.append_chunk(chunk)

            return patch_response(upload)
