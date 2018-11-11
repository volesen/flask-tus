import pytest

from .app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='class')
def class_client(request):
    app = create_app()
    # inject class variables
    request.cls.app = app
    request.cls.client = request.cls.app.test_client()
    yield
