import os

from flask import Flask, render_template

from flask_tus.views import FlaskTus

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads')
UPLOAD_VIEW = '/files/'


def create_app():
    app = Flask(__name__)
    app.config['TUS_UPLOAD_DIR'] = UPLOAD_DIR
    app.config['TUS_UPLOAD_URL'] = UPLOAD_VIEW
    TUS = FlaskTus(app)
    TUS.init_app(app)
    return app


app = create_app()


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
