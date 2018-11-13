import datetime
import os
import uuid

import mongoengine
from flask import current_app

from ..file import File
from ..models import BaseTusUpload


class Upload(mongoengine.Document, BaseTusUpload):
    created_on = mongoengine.DateTimeField(default=datetime.datetime.now)
    offset = mongoengine.IntField(default=0)
    length = mongoengine.IntField(required=True)
    file_reference = mongoengine.StringField()  # Path to file in FS

    @classmethod
    def create(cls, upload_length):
        filename = os.path.join(current_app.config['TUS_UPLOAD_DIR'], uuid.uuid4().hex)
        return cls.objects.create(length=upload_length, file_reference=filename)

    @classmethod
    def get(cls, upload_id):
        return cls.objects.get(pk=upload_id)

    @property
    def upload_id(self):
        # Uses document id as upload_id
        return str(self.id)

    def append_chunk(self, chunk):
        file = self.file  # Get FS proxy
        file.open(mode='ab')  # mode = append+binary
        file.write(chunk)
        file.close()
        self.modify(inc__offset=len(chunk))  # Increment offset

    @property
    def file(self):
        return File(self.file_reference)

    @property
    def expires(self):
        return self.created_on + current_app.config['TUS_TIMEDELTA']

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires
