import hashlib

from mongoengine import StringField
from mongoengine import BooleanField

from .mongoengine_upload import MongoengineUpload


class CustomUpload(MongoengineUpload):
    # TODO Add owner field
    # owner = mongoengine.ReferenceField(User, required=False)
    _md5 = StringField()
    valid = BooleanField()
    validation_error = StringField(default='')

    def append_chunk(self, chunk):
        # Append chunk and clear MD5 if set
        super().append_chunk(self, chunk)
        self.modify(unset__md5=1)

    @property
    def md5(self):
        if hasattr(self._md5, None) is None:
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)

            # Set MD5 fied to digest      
            self.modify(set___md5 = md5.hexdigest())

        return self._md5
