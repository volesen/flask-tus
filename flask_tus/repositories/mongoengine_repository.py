import datetime

from flask import current_app
from mongoengine import DoesNotExist
from mongoengine.errors import ValidationError

from .base_repository import BaseRepository
from ..exceptions import TusError


class MongoengineRepository(BaseRepository):

    def __init__(self, model, db):
        super(MongoengineRepository, self).__init__(model, db)

    def create(self, *args, **kwargs):
        return self.model.objects.create(*args, **kwargs)

    def find_by(self, *args,  **kwargs):
        return self.model.objects.filter(*args, **kwargs)

    def find_by_id(self, uuid):
        try:
            return self.model.objects.get(upload_uuid=uuid)
        except (DoesNotExist, ValidationError):
            # If object_id is not valid or resource does not exist
            return None

    def delete_expired(self):
        self.model.objects(created_on__lte=datetime.datetime.now() -
                           current_app.config['TUS_EXPIRATION']).delete()
