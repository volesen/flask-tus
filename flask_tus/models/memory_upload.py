import datetime
import os
import uuid

from flask import current_app

from .base_model import BaseTusUpload
from ..storage.file_system import FileSystem
from ..utilities import get_extension


class MemoryUpload(BaseTusUpload):
    """ Saves upload state in memory and uploaded file in filesystem """
    uploads = {}
    upload_id = None
    created_on = datetime.datetime.now()
    offset = 0

    def __init__(self, length=None, metadata=None):
        self.upload_id = str(uuid.uuid4())

        filename = os.path.join(current_app.config['TUS_UPLOAD_DIR'], self.upload_id)
        if metadata and metadata.get('file_name'):
            filename = filename + '.' + get_extension(metadata.get('file_name'))

        # length has to be included on HEAD request and response
        self.file = FileSystem(filename)
        self.length = length
        self.metadata = metadata
        self.__class__.uploads[self.upload_id] = self

    def append_chunk(self, chunk):
        self.file.open(mode='ab')
        self.file.write(chunk)
        self.file.close()
        self.offset += len(chunk)

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
