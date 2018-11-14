import os

from flask import Flask, render_template

from flask_tus.views import FlaskTus

app = Flask(__name__)

app.config['TUS_UPLOAD_DIR'] = os.getcwd() + '/storage/uploads'
app.config['TUS_UPLOAD_URL'] = '/files/'
app.config['TUS_MAX_SIZE'] = 2 ** 32  # 4GB

flask_tus = FlaskTus(app)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
