class BaseTusModel(object):
    """Base for upload models"""
    upload_uuid = None
    offset = None
    file = None
    path = None
    filename = None
    length = None
    metadata = None
    created_on = None

    def append_chunk(self, chunk):
        raise NotImplementedError

    @property
    def expires(self):
        raise NotImplementedError

    @property
    def expired(self):
        raise NotImplementedError
