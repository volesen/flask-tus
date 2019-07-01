class BaseRepository(object):
    """ Base class for repositories """
    model = None
    db = None

    def __init__(self, model, db):
        self.model = model
        self.db = db

    def create(self, **kwargs):
        """Crate instance and save model"""
        raise NotImplementedError

    def find_by(self, *args, **kwargs):
        """Find instances by *args and **kwargs"""
        raise NotImplementedError

    def find_by_id(self, id):
        """Find instance by model id"""
        raise NotImplementedError

    def delete_expired(self):
        raise NotImplementedError
