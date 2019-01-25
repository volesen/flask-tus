from .mongoengine_repository import MongoengineRepository
from ..models import MongoengineBaseUpload
from ..exceptions import TusError


class Repo:
    ''' Repository factory '''

    def __init__(self, model):
        if isinstance(model(), MongoengineBaseUpload):
            self.__class__ = MongoengineRepository
            self.model = model
        else:
            raise Exception
