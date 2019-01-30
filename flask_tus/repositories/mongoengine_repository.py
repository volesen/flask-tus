import os
import uuid

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

    def find_all(self):
        return self.model.objects.all()

    def find_by(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def find_by_id(self, id):
        try:
            return self.model.objects.get(pk=id)
        except (DoesNotExist, ValidationError):
            # If object_id is not valid or resource does not exist
            return None

    def instantiate(self, **kwargs):
        return self.model(**kwargs)

    def create(self, length, metadata):
        path = os.path.join(
            current_app.config['TUS_UPLOAD_DIR'], str(uuid.uuid4()))

        filename = ''

        if metadata and metadata.get('filename'):
            filename = metadata.get('filename')
            path += '.' + get_extension(filename)
            del metadata['filename']

        if length:
            length = int(length)

        return self.model.objects.create(length=length, path=path, filename=filename, metadata=metadata)

    def save(self, instance, boolean=True):
        if not isinstance(instance, self.model):
            raise TusError(500, "Instance mismatch", "Exception")

        if boolean:
            try:
                instance.save()
                return True
            except Exception:
                return False

        return instance.save()

    def update(self, instance, boolean=True, **kwargs):
        if not isinstance(instance, self.model):
            raise TusError(500, "Instance mismatch", "Exception")

        if boolean:
            try:
                instance.update(**kwargs)
                return True
            except Exception:
                return False

        return instance.update(**kwargs)
