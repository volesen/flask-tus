import datetime
import os
import uuid

from flask import abort

from flask_tus.file import File

TIME_DELTA = datetime.timedelta(days=1)  # TODO: Move to config


def generate_id():
    return uuid.uuid4().hex


class TusUpload(object):
    upload_id = generate_id()  # Primary key
    created_on = datetime.datetime.now()
    offset = 0

    def __init__(self, upload_dir, length=None):
        # Content-Length has to be included on HEAD request and response
        filename = os.path.join(upload_dir, self.upload_id)
        print(filename)
        self.file = File(filename)
        self.length = length

    def append_chunk(self, chunk):
        self.file.open(mode='ab')  # mode = append+binary
        self.offset += len(chunk)  # Size of chunk
        self.file.write(chunk)
        self.file.close()

    @property
    def expires(self):
        return self.created_on + TIME_DELTA

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires


class TusUploads(object):
    # Collection for upload resources
    uploads = {}

    def __init__(self, upload_dir):
        self.upload_dir = upload_dir

    def create_upload(self, upload_length):
        new_upload = TusUpload(self.upload_dir, upload_length)
        self.uploads[new_upload.upload_id] = new_upload
        return new_upload

    def get_upload_or_404(self, upload_id):
        upload = self.uploads.get(upload_id)
        if upload is None:
            abort(404)
        return upload
