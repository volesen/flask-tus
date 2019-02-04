import os
import datetime

from flask import Flask, render_template
from flask_mongoengine import MongoEngine

from flask_tus import FlaskTus
from flask_tus.models import MongoengineModel


app = Flask(__name__)

app.config.update({
    'TUS_UPLOAD_DIR': os.getcwd() + '/example/uploads',
    'TUS_EXPIRATION': datetime.timedelta(days=1),
    'MONGODB_SETTINGS': {
        'db': os.environ.get('DB_NAME', 'tus_dev'),
        'host': os.environ.get('DB_HOST', 'mongodb'),
        'port': int(os.environ.get('DB_PORT', 27017)),
    }
})


db = MongoEngine(app)
flask_tus = FlaskTus(app, model=MongoengineModel, db=db)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
