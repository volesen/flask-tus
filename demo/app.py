import os
import datetime

from mongoengine import StringField
from flask_mongoengine import MongoEngine
from flask import Flask, render_template
from flask_tus import FlaskTus
from flask_tus.models.mongoengine_upload import MongoengineUpload

app = Flask(__name__)
app.config['TUS_UPLOAD_DIR'] = os.getcwd() + '/storage/uploads'
app.config['TUS_UPLOAD_URL'] = '/files/'
app.config['TUS_MAX_SIZE'] = 2 ** 32  # 4GB
app.config['TUS_TIMEDELTA'] = datetime.timedelta(days=1)
app.config['TUS_COLLECTION_NAME'] = 'files_upload'
app.config['MONGODB_SETTINGS'] = {
    'db': os.environ.get('DB_NAME', 'tus_dev'),
    'host': os.environ.get('DB_HOST', 'database'),
    'port': int(os.environ.get('DB_PORT', 27017)),
}

# TODO find the way to extend model and execute callbacks
# class MongoengineUploadExtended(MongoengineUpload):
#     xxx = StringField()


mongodb = MongoEngine(app)
flask_tus = FlaskTus(app, model=MongoengineUpload)
# flask_tus = FlaskTus(app, model=MongoengineUploadExtended)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=80)
