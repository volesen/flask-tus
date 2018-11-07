from flask import Flask

from flask_tus.views import FlaskTus


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    flask_tus = FlaskTus(app)
    flask_tus.init_app(app)
    return app
