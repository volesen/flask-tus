import datetime
import os
import uuid

from flask import current_app

from ..file import File
from ..models import BaseTusUpload


class MemoryUpload(BaseTusUpload):
    """ Saves upload state in memory and uploaded file in filesystem """
    uploads = {}
    upload_id = uuid.uuid4().hex
    created_on = datetime.datetime.now()
    offset = 0

    def __init__(self, upload_dir, length=None):
        # Content-Length has to be included on HEAD request and response
        self.__class__.uploads[self.upload_id] = self
        self.file = File(os.path.join(upload_dir, self.upload_id))
        self.length = length

    def append_chunk(self, chunk):
        self.file.open(mode='ab')  # mode = append+binary
        self.file.write(chunk)
        self.file.close()
        self.offset += len(chunk)  # Size of chunk

    def get(self, upload_id):
        return self.__class__.uploads.get(upload_id)

    @classmethod
    def create(cls, upload_length):
        return cls(current_app.config['TUS_UPLOAD_DIR'], length=upload_length)

    @property
    def expires(self):
        return self.created_on + current_app.config['TUS_TIMEDELTA']

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires
