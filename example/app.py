import os
import datetime

from flask import Flask, render_template
from flask_mongoengine import MongoEngine

from flask_tus import FlaskTus
from flask_tus.models import MongoengineUpload


app = Flask(__name__)

app.config['TUS_UPLOAD_DIR'] = os.getcwd() + '/example/uploads'
app.config['TUS_TIMEDELTA'] = datetime.timedelta(days=1)

app.config['MONGODB_SETTINGS'] = {
    'db': os.environ.get('DB_NAME', 'tus_dev'),
    'host': os.environ.get('DB_HOST', 'mongodb'),
    'port': int(os.environ.get('DB_PORT', 27017)),
}


mongodb = MongoEngine(app)
flask_tus = FlaskTus(app, model=MongoengineUpload)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
