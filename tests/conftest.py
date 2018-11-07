import pytest

from .app import create_app


@pytest.fixture
def app():
    app = create_app('configs.TestConfig')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='class')
def class_client(request):
    app = create_app('configs.TestConfig')

    # inject class variables
    request.cls.client = app.test_client()
    yield
