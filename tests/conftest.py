import tempfile

import pytest

from .app import create_app


class TestConfig(object):
    TESTING = True
    UPLOAD_DIR = tempfile.mkdtemp()
    UPLOAD_VIEW = '/files/'


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['UPLOAD_DIR'] = tempfile.mkdtemp()
    app.config['UPLOAD_VIEW'] = '/files/'
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='class')
def class_client(request):
    # inject class variables
    app = create_app(TestConfig)
    app.config['TESTING'] = True
    request.cls.client = app.test_client()
    yield
