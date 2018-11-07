import os

from flask import Flask

from flask_tus.views import FlaskTus


class Config(object):
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    TESTING = True
    UPLOAD_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads')
    UPLOAD_VIEW = '/files/'


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    flask_tus = FlaskTus(app)
    flask_tus.init_app(app)
    return app
