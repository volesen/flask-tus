import os
import uuid
import datetime
import mongoengine

from flask import current_app
from .base_model import BaseTusUpload
from ..storage.file_system import FileSystem


class MongoengineUpload(mongoengine.Document, BaseTusUpload):
    offset = mongoengine.IntField(default=0)
    length = mongoengine.IntField(required=True)
    file_reference = mongoengine.StringField()  # Path to file in FS
    created_on = mongoengine.DateTimeField(default=datetime.datetime.now)
    metadata = mongoengine.DictField()

    @classmethod
    def create(cls, upload_length):
        filename = os.path.join(current_app.config['TUS_UPLOAD_DIR'], uuid.uuid4().hex)
        return cls.objects.create(length=upload_length, file_reference=filename)

    @classmethod
    def get(cls, upload_id):
        return cls.objects.get(pk=upload_id)

    @property
    def upload_id(self):
        return str(self.id)

    def append_chunk(self, chunk):
        file = self.file()
        file.open(mode='ab')
        file.write(chunk)
        file.close()
        # Increment offset
        self.modify(inc__offset=len(chunk))

    def file(self):
        return FileSystem(self.file_reference)

    @property
    def expires(self):
        return self.created_on + current_app.config['TUS_TIMEDELTA']

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires
