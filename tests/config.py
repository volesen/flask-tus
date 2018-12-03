from datetime import timedelta
from tempfile import mkdtemp


class BaseTestConfig:
    TESTING = True
    TUS_UPLOAD_DIR = mkdtemp()
    TUS_UPLOAD_VIEW = '/files/'
    TUS_MAX_SIZE = 2 ** 32
    TUS_TIMEDELTA = timedelta(days=1)


class MemoryUploadConfig(BaseTestConfig):
    pass
