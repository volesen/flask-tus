from .mongoengine_repository import MongoengineRepository
from ..models import MongoengineBaseUpload
from ..exceptions import TusError


class Repo:
    ''' Repository factory '''

    def __init__(self, model, db):
        if isinstance(model(), MongoengineBaseUpload):
            self.__class__ = MongoengineRepository
            self.__init__(model, db)
        else:
            raise Exception
