import hashlib
import datetime

from flask import current_app
from mongoengine import StringField, BooleanField, DateTimeField, signals

from ..utilities import read_chunks
from .mongoengine_base_model import MongoengineBaseModel


class MongoengineModel(MongoengineBaseModel):
    """Model to support features used at DTU Food"""
    # TODO Add owner field
    # owner = mongoengine.ReferenceField(User, required=False)
    md5 = StringField()
    filename = StringField(length=255, required=True)
    fingerprint = StringField(length=255)
    valid = BooleanField()
    validation_error = StringField(default='')
    modified_on = DateTimeField(default=datetime.datetime.now)

    def append_chunk(self, chunk):
        # Append chunk and clear MD5 if set
        super().append_chunk(chunk)
        # Seletes value of _md5 field
        self.modify(unset__md5=1)

    def update_md5(self):
        if self.md5 is None:
            md5 = hashlib.md5()
            with self.file.open() as file:
                for chunk in read_chunks(file, current_app.config['TUS_CHUNK_SIZE']):
                    md5.update(chunk)

            # Set MD5 fied to digest
            self.modify(set__md5=md5.hexdigest())

        return self.md5

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        document.modify(set__modified_on=datetime.datetime.now())


signals.post_save.connect(MongoengineModel.post_save, sender=MongoengineModel)
