import pytest

from .app import create_app, TestConfig


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
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
