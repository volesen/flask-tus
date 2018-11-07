import tempfile


class TestConfig(object):
    TESTING = True
    UPLOAD_DIR = tempfile.mkdtemp()
    UPLOAD_VIEW = '/files/'
    TUS_MAX_SIZE = 2 ** 32  # 4 gigabytes
