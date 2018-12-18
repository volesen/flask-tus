class BaseRepository(object):
    """This class is an interface"""
    model = None

    def __init__(self, model):
        self.model = model

    def instantiate(self, **kwargs):
        """Crate instance of a model"""
        pass

    def create(self, **kwargs):
        """Crate instance and save model"""
        pass

    def save(self, instance, boolean=True):
        """Save instance of model"""
        pass

    def update(self, instance, **kwargs):
        """Update already saved instance of model"""
        pass

    def find_by(self, **kwargs):
        """Find instances by **kwargs"""
        pass

    def find_all(self, id):
        """Find all instances"""
        pass

    def find_by_id(self, id):
        """Find instance by model id"""
        pass
