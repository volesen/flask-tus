import uuid
import datetime

from flask import current_app
from mongoengine import Document, IntField, DictField, StringField, DateTimeField, UUIDField

from .base_model import BaseTusModel
from ..exceptions import TusError
from ..storage.file_wrapper import FileWrapper


class MongoengineBaseModel(Document, BaseTusModel):
    upload_uuid = UUIDField(binary=False, default=uuid.uuid4, unique=True, required=True)
    path = StringField(max_length=255, required=True)
    length = IntField()
    offset = IntField(default=0, required=True)
    metadata = DictField()
    created_on = DateTimeField(default=datetime.datetime.now, required=True)

    def append_chunk(self, chunk):
        # Append chunk and increment offset on succes

        current_app.flask_tus.pre_save()
        try:
            FileWrapper(self.path).append_chunk(chunk)
        except OSError as e:
            raise TusError(500)
        else:
            # Increment offset
            self.modify(inc__offset=len(chunk))
            current_app.flask_tus.post_save()

    @property
    def file(self):
        return FileWrapper(self.path)

    @property
    def expires(self):
        return self.created_on + current_app.config['TUS_EXPIRATION']

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires

    def delete(self, *args, **kwargs):
        # On unsuccessful deletion raise "500 Internal Server Error"
        current_app.flask_tus.pre_delete()
        try:
            FileWrapper(self.path).delete()
        except OSError:
            raise TusError(500)
        else:
            super(MongoengineBaseModel, self).delete(*args, **kwargs)
            current_app.flask_tus.post_delete()

    meta = {
        'strict': False,
        'collection': 'uploads',
        'allow_inheritance': True,
        'indexes': ['upload_uuid']
    }
