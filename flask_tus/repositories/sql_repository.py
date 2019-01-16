from ..exceptions import TusError
from .base_repository import BaseRepository


class MongoengineRepository(BaseRepository):

    def __init__(self, model):
        if "mongoengine.base" not in str(model.__class__):
            raise TusError(500, "Model doesn't match mongoengine class", "Exception")

        super(MongoengineRepository, self).__init__(model)

    def find_all(self):
        return self.model.objects.all()

    def find_by(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def find_by_id(self, id):
        return self.model.objects.get(id=id)

    def instantiate(self, **kwargs):
        return self.model(**kwargs)

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def save(self, instance, boolean=True):
        if not isinstance(instance, self.model):
            raise TusError(500, "Instance mismatch", "Exception")

        if boolean:
            try:
                instance.save()
                return True
            except Exception:
                return False

        return instance.save()

    def update(self, instance, boolean=True, **kwargs):
        if not isinstance(instance, self.model):
            raise TusError(500, "Instance mismatch", "Exception")

        if boolean:
            try:
                instance.update(**kwargs)
                return True
            except Exception:
                return False

        return instance.update(**kwargs)
