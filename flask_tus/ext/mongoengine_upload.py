import datetime

import mongoengine
from flask import current_app

from ..file import File
from ..models import BaseTusUpload


class Upload(mongoengine.Document, BaseTusUpload):
    created_on = mongoengine.DateTimeField(default=datetime.datetime.now)
    offset = mongoengine.IntField(default=0)
    length = mongoengine.IntField(required=True)
    file_reference = mongoengine.StringField()  # Path to file in FS
    meta = {'db-alias': current_app.config.get('TUS_MODEL_DB')}

    @classmethod
    def create(cls, upload_length):
        # Custom constructor
        upload = cls(length=upload_length)
        upload.save()
        return upload

    def get(self, upload_id):
        return self.objects.get(id=upload_id)

    @property
    def upload_id(self):
        # Uses document id as upload_id
        return self.id

    def append_chunk(self, chunk):
        self.file.open(mode='ab')  # mode = append+binary
        self.file.write(chunk)
        self.file.close()
        self.offset += len(chunk)  # Size of chunk

    @property
    def file(self):
        return File(self.file_reference)

    @property
    def expires(self):
        return self.created_on + current_app.config['TUS_TIMEDELTA']

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires
