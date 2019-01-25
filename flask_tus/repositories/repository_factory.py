from .mongoengine_repository import MongoengineRepository
from ..models import MongoengineBaseUpload
from ..exceptions import TusError


def repo(model):
    if isinstance(model(), MongoengineBaseUpload):
        return MongoengineRepository(model)
    else:
        raise TusError('Model not supported')
