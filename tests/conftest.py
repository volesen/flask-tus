import mongoengine
import pytest
from flask import Flask

from flask_tus import FlaskTus
from .config import MongoUploadConfig


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)
    flask_tus = FlaskTus()
    mongoengine.connect('mongoenginetest', host='mongomock://localhost')
    flask_tus.init_app(app, model=app.config['UPLOAD_MODEL'])

    return app, flask_tus


@pytest.fixture(scope='class')
def class_client(request):
    # TODO Run tests on all models
    request.cls.app, request.cls.flask_tus = create_app(MongoUploadConfig)
    request.cls.client = request.cls.app.test_client()
    yield
    # Teardown here if needed
