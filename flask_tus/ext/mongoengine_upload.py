import datetime

import mongoengine
from flask import current_app

from ..file import File


class Upload(mongoengine.Document):
    created_on = mongoengine.DateTimeField(default=datetime.datetime.now)
    offset = mongoengine.IntField(default=0)
    length = mongoengine.IntField(required=True)
    file_reference = mongoengine.StringField()  # Path to file in FS

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

    @property
    def file(self):
        return File(self.file_reference)

    @property
    def expires(self):
        return self.created_on + current_app.config['TUS_TIMEDELTA']

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires

    class meta:
        db = current_app.config.get('TUS_MODEL_DB')
