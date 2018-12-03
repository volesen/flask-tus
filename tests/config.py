from datetime import timedelta
from tempfile import mkdtemp

from flask_tus.models.memory_upload import MemoryUpload
from flask_tus.models.mongoengine_upload import MongoengineUpload


class BaseTestConfig:
    TESTING = True
    TUS_UPLOAD_DIR = mkdtemp()
    TUS_UPLOAD_VIEW = '/files/'
    TUS_MAX_SIZE = 2 ** 32
    TUS_TIMEDELTA = timedelta(days=1)


class MemoryUploadConfig(BaseTestConfig):
    UPLOAD_MODEL = MemoryUpload


class MongoUploadConfig(BaseTestConfig):
    UPLOAD_MODEL = MongoengineUpload
