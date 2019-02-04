import os
import uuid
import datetime

from flask import current_app
from mongoengine import DoesNotExist
from mongoengine.errors import ValidationError

from .base_repository import BaseRepository
from ..utilities import get_extension
from ..exceptions import TusError


class MongoengineRepository(BaseRepository):

    def __init__(self, model, db):
        if "mongoengine.base" not in str(model.__class__):
            raise TusError(
                500, "Model doesn't match mongoengine class", "Exception")

        super(MongoengineRepository, self).__init__(model, db)

    def create(self, length, metadata, **kwargs):
        path = os.path.join(
            current_app.config['TUS_UPLOAD_DIR'], str(uuid.uuid4()))

        if length:
            length = int(length)

        filename = ''
        if metadata and metadata.get('filename'):
            filename = metadata.get('filename')
            path += '.' + get_extension(filename)
            del metadata['filename']

        return self.model.objects.create(length=length, path=path, filename=filename, metadata=metadata, **kwargs)

    def find_by(self, *args,  **kwargs):
        return self.model.objects.filter(*args, **kwargs)

    def find_by_id(self, id):
        try:
            return self.model.objects.get(pk=id)
        except (DoesNotExist, ValidationError):
            # If object_id is not valid or resource does not exist
            return None

    def delete_expired(self):
        self.model.objects(created_on__lte=datetime.datetime.now() -
                           current_app.config['TUS_TIMEDELTA']).delete()
