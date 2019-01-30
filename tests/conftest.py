import pytest

from flask import Flask
from flask_tus import FlaskTus
from .config import MongoengineUploadConfig, MongoengineBaseUploadConfig, SQLAlchemyModelConfig

configs = (MongoengineUploadConfig,
           MongoengineBaseUploadConfig, SQLAlchemyModelConfig)


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    flask_tus = FlaskTus()

    model = config.model
    db = config.init_db(app)

    flask_tus.init_app(app, model=model, db=db)

    return app, flask_tus


@pytest.fixture(scope='class', params=configs)
def class_client(request):
    request.cls.app, request.cls.flask_tus = create_app(request.param)
    request.cls.client = request.cls.app.test_client()
    yield
    # Teardown here if needed
