# flask-tus

[tus](https://www.tus.io) server implementation for [Flask](https://flask.pocoo.org).

## Demo

### With pipenv:
```
git clone https://github.com/volesen/flask-tus.git
cd flask-tus
pipenv install
pipenv shell

```

### Wth virtualenviroments:
```
git clone https://github.com/volesen/flask-tus.git
cd flask-tus
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Uploading a file
```
python demo/app.py
```
Go to [127.0.0.1:8000] and upload a file. The uploaded file will end in `demo/uploads/`

## Settings
Settings are added in app.config:
- `TUS_UPLOAD_URL` - Url of endpoint
- `TUS_UPLOAD_DIR` - Path to upload directory. Can be changed with custom models (eg. for saving in AWS S3)
- `TUS_MAX_SIZE` - Max size of a file-upload
- `TUS_TIMEDELTA` - Time allowed to complete upload

## Models (WIP)
Upload states are by default saved in memory, but can be saved persistently, as in the following example:
```
from flask import Flask
from flask_tus import FlaskTus
from flask_tus.ext import mongo_upload

def create_app(config):
  app = Flask(__name__)  
  app.config.from_object(config)
  flask_tus = FlaskTus
  flask_tus.model = mongo_upload
  flask_tus.init_app()
  return app
```
