class BaseTusModel(object):
    """Base for upload models"""
    upload_id = None
    created_on = None
    offset = None
    file = None
    path = None
    filename = None
    length = None
    metadata = None

    def append_chunk(self, chunk):
        raise NotImplementedError

    @property
    def expires(self):
        raise NotImplementedError

    @property
    def expired(self):
        raise NotImplementedError
