import os
import datetime

from flask import Flask, render_template
from flask_tus import FlaskTus
from flask_tus.models.mongoengine_upload import MongoengineUpload

app = Flask(__name__)
app.config['TUS_UPLOAD_DIR'] = os.getcwd() + '/storage/uploads'
app.config['TUS_UPLOAD_URL'] = '/files/'
app.config['TUS_MAX_SIZE'] = 2 ** 32  # 4GB
app.config['TUS_TIMEDELTA'] = datetime.timedelta(days=1)

# from flask_mongoengine import MongoEngine
# app.config['MONGODB_SETTINGS'] = {
#     'db': DB_NAME,
#     'host': DB_HOST,
#     'port': DB_PORT,
# }
# mongodb = Mpngoengine(app)
# flask_tus = FlaskTus(app, mongodb)

flask_tus = FlaskTus(app, model=MongoengineUpload)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
