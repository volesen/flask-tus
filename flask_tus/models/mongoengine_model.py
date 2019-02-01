import hashlib
import datetime

from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import DateTimeField
from mongoengine import signals

from .mongoengine_base_model import MongoengineBaseModel


class MongoengineModel(MongoengineBaseModel):
    """Model to support features used at DTU Food"""
    # TODO Add owner field
    # owner = mongoengine.ReferenceField(User, required=False)
    _md5 = StringField()
    valid = BooleanField()
    filename = StringField(length=255, required=True)
    fingerprint = StringField(length=255)
    modified_on = DateTimeField(default=datetime.datetime.now)
    validation_error = StringField(default='')

    # TODO: Review this - this could be added in utils.py as a helpher func as it is also used in tests
    @staticmethod
    def __read_chunks(file, chunk_size=1024):
        return iter(lambda: file.read(chunk_size), b'')

    def append_chunk(self, chunk):
        # Append chunk and clear MD5 if set
        super().append_chunk(chunk)
        self.modify(unset___md5=1)

    @property
    def md5(self):
        if self._md5 is None:
            md5 = hashlib.md5()
            with self.file.open() as file:
                for chunk in self.__read_chunks(file):
                    md5.update(chunk)

            # Set MD5 fied to digest
            self.modify(set___md5=md5.hexdigest())

        return self._md5

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        document.modify(set__modified_on=datetime.datetime.now())


signals.post_save.connect(MongoengineModel.post_save, sender=MongoengineModel)
