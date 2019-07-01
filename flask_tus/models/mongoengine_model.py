import hashlib
import datetime

from flask import current_app
from mongoengine import StringField, BooleanField, DateTimeField, signals

from ..utilities import read_chunks
from .mongoengine_base_model import MongoengineBaseModel
from ..storage.file_wrapper import FileWrapper


class MongoengineModel(MongoengineBaseModel):
    """Model to support features used at DTU Food"""
    md5 = StringField()
    filename = StringField(length=255)#, required=True)
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
        """
            Caclulates and sets md5 hash when md5 property is accesed
        """
        if self.md5 is None:
            md5 = hashlib.md5()
            with FileWrapper(self.path, mode='rb') as f:
                for chunk in read_chunks(f, current_app.config['TUS_CHUNK_SIZE']):
                    md5.update(chunk)

            # Set MD5 field to digest
            self.modify(set__md5=md5.hexdigest())

        return self.md5

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        document.modify(set__modified_on=datetime.datetime.now())


signals.post_save.connect(MongoengineModel.post_save, sender=MongoengineModel)
