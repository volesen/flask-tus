import pytest
from flask import Flask

from flask_tus import FlaskTus
from .config import MemoryUploadConfig


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    flask_tus = FlaskTus()
    flask_tus.init_app(app)

    return app, flask_tus


@pytest.fixture(scope='class')
def class_client(request):
    request.cls.app, request.cls.flask_tus = create_app(MemoryUploadConfig)
    request.cls.client = request.cls.app.test_client()
    yield
