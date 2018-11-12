# flask-tus

[tus](https://www.tus.io) server implementation for Flask.

## Install
WIP

## Settings
Settings are added in app.config:
- `TUS_UPLOAD_URL` - Url of endpoint
- `TUS_UPLOAD_DIR` - Path to upload directory. Can be changed with custom models (eg. for saving in AWS S3)
- `TUS_MAX_SIZE` - Max size of a file-upload

## Models (WIP)
Upload states are by default saved in memory, but can be saved in a DB, with the following
```
from flask import Flask
from flask_tus import FlaskTus
from flask_tus.ext import mongo_upload

def create_app(config):
  app = Flask(__name__)  
  app.config.fromObject(config)
  flask_tus = FlasTus()
  flask_tus.model = mongo_upload
  flask_tus.init_app()
  return app
```
