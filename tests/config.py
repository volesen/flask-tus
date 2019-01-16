import mongoengine

from tempfile import mkdtemp
from datetime import timedelta

from flask_tus.models import MemoryUpload, MongoengineBaseUpload, MongoengineUpload


class BaseTestConfig:
    TESTING = True
    TUS_UPLOAD_DIR = mkdtemp()
    TUS_UPLOAD_VIEW = '/files/'
    TUS_MAX_SIZE = 2 ** 32
    TUS_TIMEDELTA = timedelta(days=1)


class MemoryUploadConfig(BaseTestConfig):
    UPLOAD_MODEL = MemoryUpload

    @classmethod
    def init_db(cls):
        pass


class MongoengineBaseUploadConfig(BaseTestConfig):
    UPLOAD_MODEL = MongoengineBaseUpload

    @classmethod
    def init_db(cls):
        mongoengine.connect('mongoenginetest', host='mongomock://localhost')


class MongoengineUploadConfig(MongoengineBaseUploadConfig):
    UPLOAD_MODEL = MongoengineUpload
