class BaseTusUpload(object):
    """Upload interface"""
    upload_id = None
    created_on = None
    offset = None
    file = None
    length = None
    metadata = None

    def create(self, upload_length, metadata=None):
        raise NotImplementedError

    def get(self, upload_id):
        raise NotImplementedError

    def append_chunk(self, chunk):
        raise NotImplementedError

    @property
    def expires(self):
        raise NotImplementedError

    @property
    def expired(self):
        raise NotImplementedError
