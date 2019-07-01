import tempfile
import datetime

from flask import request

import flask_tus.responses as Response

from .utilities import extract_metadata
from .exceptions import TusError
from .repositories import Repo
from .responses import (option_response, post_response,
                        head_response, patch_response, delete_response)
from .validators import (validate_post, validate_head,
                         validate_patch, validate_delete, validate_metadata)


class FlaskTus(object):
    def __init__(self, app=None, model=None, db=None, repo=None):
        if app:
            self.app = app
            self.init_app(app, model, db, repo)

    # Application factory

    def init_app(self, app, model, db=None, repo=None):
        app.config.setdefault('TUS_UPLOAD_DIR', tempfile.mkdtemp())
        app.config.setdefault('TUS_UPLOAD_URL', '/files/')
        app.config.setdefault('TUS_MAX_SIZE', 2**32)  # 4 GB
        app.config.setdefault('TUS_EXPIRATION', datetime.timedelta(days=1))
        app.config.setdefault('TUS_CHUNK_SIZE', 2**16 ) # 8 KB

        app.register_error_handler(TusError, TusError.error_handler)

        app.add_url_rule(app.config['TUS_UPLOAD_URL'], 'create_upload',
                         self.create_upload, methods=['OPTIONS', 'POST'])
        app.add_url_rule(app.config['TUS_UPLOAD_URL'] + '<upload_uuid>',
                         'modify_upload', self.modify_upload, methods=['HEAD', 'PATCH', 'DELETE'])

        if repo:
            self.repo = repo
        else:
            # Repository factory
            self.repo = Repo(model, db)

        # Inject flask_tus as property to support CLI commands
        app.flask_tus = self

    def create_upload(self):
        # Get server configuration
        if request.method == 'OPTIONS':
            return option_response()

        if request.method == 'POST':
            validate_post()

            # Call callback
            self.on_create()

            # Get and typecast upload length and metadata
            upload_length = request.headers.get('Upload-Length')

            if upload_length:
                upload_length = int(upload_length)

            upload_metadata = request.headers.get('Upload-Metadata')

            if upload_metadata:
                upload_metadata = extract_metadata(upload_metadata)

                # DTU Food usecase specific features

                validate_metadata(upload_metadata)

                fingerprint = upload_metadata.get('fingerprint')

                if fingerprint:
                    # Get upload
                    upload = self.repo.find_by(fingerprint=fingerprint)

                    # If an upload has matching fingerprint
                    if upload:
                        return post_response(upload)

            upload = self.repo.create(upload_length, upload_metadata)

            return post_response(upload)

    def modify_upload(self, upload_uuid):
        upload = self.repo.find_by_id(upload_uuid)

        # Get state of a resource
        if request.method == 'HEAD':
            validate_head(upload)
            return head_response(upload)

        # Update a resource
        if request.method == 'PATCH':
            validate_patch(upload)

            chunk = request.data
            upload.append_chunk(chunk)

            if upload.offset == upload.length:
                self.on_complete()

            return patch_response(upload)

        if request.method == 'DELETE':
            validate_delete(upload)

            upload.delete()

            return delete_response()

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
