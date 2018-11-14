import os
import uuid
import datetime

from flask import current_app
from ..file import File
from ..models import BaseTusUpload


class MemoryUpload(BaseTusUpload):
    """ Saves upload state in memory and uploaded file in filesystem """
    uploads = {}
    upload_id = uuid.uuid4().hex
    created_on = datetime.datetime.now()
    offset = 0

    def __init__(self, length=None, metadata=None):
        self.__class__.uploads[self.upload_id] = self
        # length has to be included on HEAD request and response
        self.file = File(os.path.join(current_app.config['TUS_UPLOAD_DIR'], self.upload_id))
        self.length = length
        self.metadata = metadata

    def append_chunk(self, chunk):
        self.file.open(mode='ab')
        self.file.write(chunk)
        self.file.close()
        self.offset += len(chunk)  # Size of chunk

    @classmethod
    def get(cls, upload_id):
        return cls.uploads.get(upload_id)

    @classmethod
    def create(cls, upload_length, metadata):
        return cls(length=upload_length, metadata=metadata)

    @property
    def expires(self):
        return self.created_on + current_app.config['TUS_TIMEDELTA']

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires
