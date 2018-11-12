class BaseTusUpload(object):
    upload_id = None
    created_on = None
    offset = None
    file = None
    length = None

    def append_chunk(self, chunk):
        raise NotImplementedError

    def create(self, upload_length):
        raise NotImplementedError

    def get(self, upload_id):
        raise NotImplementedError

    @property
    def expires(self):
        raise NotImplementedError

    @property
    def expired(self):
        raise NotImplementedError
