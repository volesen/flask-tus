import mongoengine

from tempfile import mkdtemp
from datetime import timedelta

from flask_tus.models import MemoryUpload, MongoengineUpload, CustomUpload


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


class MongoUploadConfig(BaseTestConfig):
    UPLOAD_MODEL = MongoengineUpload

    @classmethod
    def init_db(cls):
        mongoengine.connect('mongoenginetest', host='mongomock://localhost')


class CustomUploadConfig(MongoUploadConfig):
    UPLOAD_MODEL = CustomUpload
