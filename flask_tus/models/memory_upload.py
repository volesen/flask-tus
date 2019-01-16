import os
import uuid
import datetime

from flask import current_app

from .base_model import BaseTusUpload
from ..exceptions import TusError
from ..storage.file_system import FileSystem
from ..utilities import get_extension


class MemoryUpload(BaseTusUpload):
    """ Saves upload state in memory and uploaded file in filesystem """
    objects = {}
    upload_id = None
    created_on = datetime.datetime.now()
    offset = 0

    def __init__(self, length, metadata):
        self.upload_id = str(uuid.uuid4())

        file_path = os.path.join(current_app.config['TUS_UPLOAD_DIR'], self.upload_id)
        if metadata and metadata.get('filename'):
            file_path += '.' + get_extension(metadata.get('filename'))

        self.file = FileSystem(file_path)
        self.file_path = file_path
        self.length = length
        self.metadata = metadata

        # HACK Tricky!
        self.__class__.objects[self.upload_id] = self

    def append_chunk(self, chunk):
        current_app.flask_tus.pre_save()
        try:
            with self.file.open(mode='ab') as file:
                file.write(chunk)
        except Exception as error:
            raise TusError(500, str(error))
        else:
            self.offset += len(chunk)
            current_app.flask_tus.post_save()

    @classmethod
    def get(cls, upload_id):
        return cls.objects.get(upload_id)

    @classmethod
    def create(cls, upload_length, metadata):
        """ Factory method"""
        return cls(length=upload_length, metadata=metadata)

    @property
    def expires(self):
        return self.created_on + current_app.config['TUS_TIMEDELTA']

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires

    def delete(self):
        current_app.flask_tus.pre_delete()

        try:
            self.file.delete()
        except OSError:
            raise TusError(500)
        else:
            current_app.flask_tus.post_delete()
            del self.__class__.objects[self.upload_id]

    @classmethod
    def delete_expired(cls):
        cls.objects = {upload_id: upload for upload_id, upload in cls.objects.items() if not upload.expired}
