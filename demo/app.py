import os

from flask import Flask, render_template
from flask_tus.main import FlaskTus
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['TUS_UPLOAD_DIR'] = os.getcwd() + '/storage/uploads'
app.config['TUS_UPLOAD_URL'] = '/files/'
app.config['TUS_MAX_SIZE'] = 2 ** 32  # 4GB
app.config['MONGODB_SETTINGS'] = {
    'db': DB_NAME,
    'host': DB_HOST,
    'port': DB_PORT,
}


mongodb = Mpngoengine(app)
flask_tus = FlaskTus(app, mongodb)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
