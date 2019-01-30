import datetime

from flask import current_app
from mongoengine import Document
from mongoengine import IntField
from mongoengine import DictField
from mongoengine import StringField
from mongoengine import DateTimeField

from .base_model import BaseTusUpload
from ..exceptions import TusError
from ..storage.file_system import FileSystem
from ..utilities import get_extension


class MongoengineBaseUpload(Document, BaseTusUpload):
    fingerprint = StringField()
    filename = StringField()
    path = StringField()
    offset = IntField(default=0)
    length = IntField()
    metadata = DictField()
    created_on = DateTimeField(default=datetime.datetime.now)
    # TODO
    modified_on = DateTimeField(default=datetime.datetime.now)

    meta = {
        'strict': False,
        'collection': 'uploads',
        'allow_inheritance': True
    }

    @property
    def upload_id(self):
        return str(self.id)

    def append_chunk(self, chunk):
        # Handle file and increment offset on every append
        current_app.flask_tus.pre_save()
        try:
            with self.file.open(mode='ab') as file:
                file.write(chunk)
        # except OSError:
        except Exception as error:
            raise TusError(503, str(error), 'APIError')
            # raise TusError(503, 'MongoUpload- Failed to append to a file.')
        else:
            # Increment offset
            self.modify(inc__offset=len(chunk))
            current_app.flask_tus.post_save()

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
        # On unsuccessful deletion raise "500 Internal Server Error"
        current_app.flask_tus.pre_delete()
        try:
            FileSystem(self.path).delete()
        except OSError:
            raise TusError(500)
        else:
            super(MongoengineBaseUpload, self).delete(*args, **kwargs)
            current_app.flask_tus.post_delete()
