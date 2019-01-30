import mongoengine

from tempfile import mkdtemp
from datetime import timedelta

from flask_tus.models import MongoengineBaseUpload, MongoengineUpload


class BaseTestConfig:
    TESTING = True
    TUS_UPLOAD_DIR = mkdtemp()
    TUS_UPLOAD_VIEW = '/files/'
    TUS_MAX_SIZE = 2 ** 32
    TUS_TIMEDELTA = timedelta(days=1)


class MongoengineBaseUploadConfig(BaseTestConfig):
    model = MongoengineBaseUpload

    @classmethod
    def init_db(cls):
        mongoengine.connect('test', host='mongodb', port=27017)


class MongoengineUploadConfig(MongoengineBaseUploadConfig):
    model = MongoengineUpload
