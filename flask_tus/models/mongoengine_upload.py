import datetime
import os
import uuid

import mongoengine
from flask import current_app

from .base_model import BaseTusUpload
from ..storage.file_system import FileSystem
from ..utilities import get_extension


class MongoengineUpload(mongoengine.Document, BaseTusUpload):
    # TODO Add owner field
    # owner = mongoengine.ReferenceField(User, required=False)
    path = mongoengine.StringField()
    offset = mongoengine.IntField(default=0)
    length = mongoengine.IntField(required=True)
    metadata = mongoengine.DictField()
    created_on = mongoengine.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def create(cls, upload_length, metadata=None):
        filename = os.path.join(current_app.config['TUS_UPLOAD_DIR'], str(uuid.uuid4()))

        if metadata and metadata.get('file_name'):
            filename = filename + '.' + get_extension(metadata.get('file_name'))

        return cls.objects.create(length=upload_length, path=filename, metadata=metadata)

    @classmethod
    def get(cls, upload_id):
        try:
            upload = cls.objects.get(pk=upload_id)
            return upload
        except mongoengine.DoesNotExist:
            return None

    @property
    def upload_id(self):
        return str(self.id)

    def append_chunk(self, chunk):
        # Handle file and increment offset on every append
        file = self.file
        file.open(mode='ab')
        file.write(chunk)
        file.close()
        self.modify(inc__offset=len(chunk))

    @property
    def file(self):
        return FileSystem(self.path)

    @property
    def expires(self):
        return self.created_on + current_app.config['TUS_TIMEDELTA']

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires

    def delete(self, *args, **kwargs):
        # TODO Delete file
        # REVIEW Lukasz Dynowski
        # NOTE This is a dangerous assumption. What if you don't have permissions to delete file? or you no longer have access to storage?
        # FIXME Use exceptions to handle unexpected behavior. If no error(s) is thrown then proceed with super(***).delete(****)
        FileSystem(self.path).delete()
        super(MongoengineUpload, self).delete(*args, **kwargs)

    @classmethod
    def delete_expired(cls):
        cls.objects(created_on__lte=datetime.datetime.now() - current_app.config['TUS_TIMEDELTA']).delete()
