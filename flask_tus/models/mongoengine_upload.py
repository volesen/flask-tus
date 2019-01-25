import hashlib

from mongoengine import StringField
from mongoengine import BooleanField

from .mongoengine_base_upload import MongoengineBaseUpload


class MongoengineUpload(MongoengineBaseUpload):
    # TODO Add owner field
    # owner = mongoengine.ReferenceField(User, required=False)
    _md5 = StringField()
    valid = BooleanField()
    validation_error = StringField(default='')
    fingerprint = StringField()

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
