import tempfile
import datetime

import flask_tus.responses as Response
import flask_tus.validators as Validator

from flask import request
from flask_tus.exceptions import TusError
from flask_tus.utilities import extract_metadata
from flask_tus.repositories import Repo


class FlaskTus(object):
    app = None
    repo = None

    def __init__(self, app=None, model=None, db=None, repo=None):
        if app:
            self.app = app
            self.init_app(app, model, db)

    # Application factory

    def init_app(self, app, model, db=None, repo=None):
        app.config.setdefault('TUS_UPLOAD_DIR', tempfile.mkdtemp())
        app.config.setdefault('TUS_UPLOAD_URL', '/files/')
        app.config.setdefault('TUS_MAX_SIZE', 2**32)  # 4GB
        app.config.setdefault('TUS_TIMEDELTA', datetime.timedelta(days=1))

        app.register_error_handler(TusError, TusError.error_handler)

        app.add_url_rule(app.config['TUS_UPLOAD_URL'], 'create_upload',
                         self.create_upload, methods=['OPTIONS', 'POST'])
        app.add_url_rule(app.config['TUS_UPLOAD_URL'] + '<upload_id>',
                         'modify_upload', self.modify_upload, methods=['HEAD', 'PATCH', 'DELETE'])

        if repo:
            self.repo = repo
        else:
            # Repository factory
            self.repo = Repo(model, db)

        # Inject flask_tus ass property to support CLI commands
        app.flask_tus = self

    def create_upload(self):
        # Get server configuration
        if request.method == 'OPTIONS':
            return Response.option_response()

        if request.method == 'POST':
            Validator.validate_post()

            # Call callback
            self.on_create()

            upload_length = request.headers.get('Upload-Length')
            upload_metadata = request.headers.get('Upload-Metadata')

            if upload_metadata:
                upload_metadata = extract_metadata(upload_metadata)
                fingerprint = upload_metadata.get('fingerprint')

                if fingerprint:
                    # If fingerprint is set
                    upload = self.repo.find_by(fingerprint=fingerprint)

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
