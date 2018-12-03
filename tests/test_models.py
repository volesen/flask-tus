import pytest

from flask_tus.models.base_model import BaseTusUpload
from flask_tus.models.memory_upload import MemoryUpload
from flask_tus.storage.base_file import BaseFile

# from flask_tus.models.mongoengine_upload import MongoengineUpload

models = (MemoryUpload)


# @pytest.mark.parametrize("model", models)
@pytest.mark.usefixtures('class_client')
class TestModels:
    # TODO: Parametrize so it can test over collection of models

    def test_create(self):
        with self.app.app_context():
            # self.app.flask_tus.model = model
            upload = self.app.flask_tus.model.create(None, None)
            assert isinstance(upload, BaseTusUpload)

    def test_get(self):
        with self.app.app_context():
            # Create and get upload and assert it is an instance of BaseTusUpload
            upload_id = self.app.flask_tus.model.create(None, None).upload_id

            upload = self.app.flask_tus.model.get(upload_id)
            assert isinstance(upload, BaseTusUpload)

    def test_file(self):
        with self.app.app_context():
            upload = self.app.flask_tus.model.create(None, None)
            assert isinstance(upload.file, BaseFile)
