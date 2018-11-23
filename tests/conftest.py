import pytest

from flask import Flask
from flask_tus import FlaskTus
from datetime import timedelta
from tempfile import mkdtemp


def create_app():
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'TUS_UPLOAD_DIR': mkdtemp(),
        'TUS_UPLOAD_VIEW': '/files/',
        'TUS_MAX_SIZE': 2 ** 32,  # 4 gigabytes
        'TUS_TIMEDELTA': timedelta(days=1)
    })

    flask_tus = FlaskTus()
    flask_tus.init_app(app)

    return app, flask_tus


@pytest.fixture
def app():
    app, flask_tus = create_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='class')
def class_client(request):
    request.cls.app, request.cls.flask_tus = create_app()
    request.cls.client = request.cls.app.test_client()
    yield
