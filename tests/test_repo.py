import pytest

from flask_tus.models.base_model import BaseTusModel
from flask_tus.storage.base_file import BaseFile


@pytest.mark.usefixtures('class_client')
class TestRepo:
    def test_create(self):
        with self.app.app_context():
            # self.app.flask_tus.model = model
            upload = self.app.flask_tus.repo.create(length=0, metadata=None, path='')

            assert isinstance(upload, BaseTusModel)

    def test_get(self):
        with self.app.app_context():
            # Create and get upload and assert it is an instance of BaseTusUpload
            upload_uuid = self.app.flask_tus.repo.create(length=0, metadata=None, path='').upload_uuid
            upload = self.app.flask_tus.repo.find_by_id(upload_uuid)

            assert isinstance(upload, BaseTusModel)

    def test_file(self):
        with self.app.app_context():
            upload = self.app.flask_tus.repo.create(length=0, metadata=None, path='')

            assert isinstance(upload.file, BaseFile)
