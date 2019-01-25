import flask_tus.responses as Response
import flask_tus.validators as Validator

from tempfile import mkdtemp
from flask import request
from flask_tus.exceptions import TusError
from flask_tus.models.mongoengine_upload import MongoengineUpload
from flask_tus.utilities import extract_metadata
from flask_tus.repositories import MongoengineRepository


class FlaskTus(object):
    app = None
    model = None
    repo = None

    def __init__(self, app=None, model=MongoengineUpload):
        if app:
            self.app = app
            self.init_app(app, model)

    # Application factory

    def init_app(self, app, model=MongoengineUpload):
        app.config.setdefault('TUS_UPLOAD_DIR', mkdtemp())
        app.config.setdefault('TUS_UPLOAD_URL', '/files/')

        app.register_error_handler(TusError, TusError.error_handler)

        app.add_url_rule(app.config['TUS_UPLOAD_URL'], 'create_upload',
                         self.create_upload, methods=['OPTIONS', 'POST'])
        app.add_url_rule(app.config['TUS_UPLOAD_URL'] + '<upload_id>',
                         'modify_upload', self.modify_upload, methods=['HEAD', 'PATCH', 'DELETE'])

        self.repo = MongoengineRepository(model)
        self.model = model
        app.flask_tus = self

    def create_upload(self):
        # Get server configuration
        if request.method == 'OPTIONS':
            return Response.option_response()

        if request.method == 'POST':
            Validator.validate_post()

            # Crate a resource callback
            self.on_create()

            upload_length = request.headers.get('Upload-Length')
            upload_metadata = request.headers.get('Upload-Metadata')

            if upload_metadata:
                upload_metadata = extract_metadata(upload_metadata)

            upload = self.repo.create(upload_length, upload_metadata)

            return Response.post_response(upload)

    def modify_upload(self, upload_id):
        upload = self.repo.find_by_id(upload_id)

        # Get state of a resource
        if request.method == 'HEAD':
            Validator.validate_head(upload)
            return Response.head_response(upload)

        # Update a resource
        if request.method == 'PATCH':
            Validator.validate_patch(upload)

            chunk = request.data
            upload.append_chunk(chunk)

            if upload.offset == int(upload.length):
                self.on_complete()

            return Response.patch_response(upload)

        if request.method == 'DELETE':
            Validator.validate_delete(upload)

            upload.delete()

            return Response.delete_response()

    def on_create(self):
        # Callback for creation of upload
        pass

    def pre_save(self):
        # Callback for pre-save on each chunk
        pass

    def post_save(self):
        # Callback for post-save on each chunk
        pass

    def on_complete(self):
        # Callback for completion of upload
        pass

    def pre_delete(self):
        # Callback for pre-delete of upload
        pass

    def post_delete(self):
        # Callback for post-delete of upload
        pass
