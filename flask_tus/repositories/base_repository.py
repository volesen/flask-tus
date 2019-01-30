class BaseRepository(object):
    """This class is an interface"""
    model = None
    db = None

    def __init__(self, model, db):
        self.model = model
        self.db = db

    def instantiate(self, **kwargs):
        """Crate instance of a model"""
        raise NotImplementedError

    def create(self, **kwargs):
        """Crate instance and save model"""
        raise NotImplementedError

    def save(self, instance, boolean=True):
        """Save instance of model"""
        raise NotImplementedError

    def update(self, instance, **kwargs):
        """Update already saved instance of model"""
        raise NotImplementedError

    def find_by(self, **kwargs):
        """Find instances by **kwargs"""
        raise NotImplementedError

    def find_all(self, id):
        """Find all instances"""
        raise NotImplementedError

    def find_by_id(self, id):
        """Find instance by model id"""
        raise NotImplementedError

    def delete_expired(self):
        raise NotImplementedError
