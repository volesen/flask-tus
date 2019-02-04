# flask-tus
[tus](https://www.tus.io) server implementation for [Flask](https://flask.pocoo.org).

# Requirements
Following software stack is required to run this project:
* [python3](https://www.python.org/)
* [pipenv](https://pipenv.readthedocs.io/en/latest/)
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)
* [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/)

If Docker is not used, a Mongoengine database is required for testing and running the example. Furthermore, the host has to be changed in `tests/config.py` and `example/app.py` respectively.

# Installation

### pipenv
```bash
$ git clone https://github.com/volesen/flask-tus.git
$ cd flask-tus
# pipenv --python $(which python3) install
$ pipenv --python /path/to/python3 install
$ pipenv shell
```

### virtualenviroment
```bash
$ git clone https://github.com/volesen/flask-tus.git
$ cd flask-tus
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ python setup.py install
```

### docker
```bash
$ git clone https://github.com/volesen/flask-tus.git
$ cd flask-tus
$ docker-compose -f docker-compose.yml up
```

## Running example

### Python
```bash
$ python demo/app.py
```
### Docker

```bash
$ docker-compose  up
```

Go to [127.0.0.1:5000](http://127.0.0.1:5000) and upload a file. The uploaded file will end in `demo/uploads/`

## Testing

### Python
```bash
$ pytest tests
```

### Docker

```bash
$ docker-compose run app pytest tests
```

# Usage

The flask_tus extension, need to be instatiated with an app and a model and optionally a database/session object, in the case of SQLAlchemy-models, as in the following example:

```python
from flask import Flask
from flask_sqlachemy import SQLAlchemy

from flask_tus import FlaskTus
from flask_tus.models import SQLAlchemyModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

flask_tus = FlaskTus(app, model=SQLAlchemyModel, db=db)
```

The flask_tus extensions supports the applicaiton facotry pattern, with the `flask_tus.init_app` method.

## Settings
Settings are added in app.config:
* `TUS_UPLOAD_URL` - Url of endpoint
* `TUS_UPLOAD_DIR` - Path to upload directory. Can be changed with custom models (eg. for saving in AWS S3)
* `TUS_MAX_SIZE` - Max size of a file-upload
* `TUS_EXPIRATION` - Time allowed to complete upload (Must be insatce of datetime.timedelta)
* `TUS_CHUNK_SIZE` - Chunk size used in calculation of MD5 


## Callbacks
The callbacks are as follows:
* `FlaskTus.on_create` - Callback for creation of upload
* `FlaskTus.pre_save` - Callback for pre-save on each chunk
* `FlaskTus.post_save` - Callback for post-save on each chunk
* `FlaskTus.on_complete` - Callback for completion of upload
* `FlaskTus.pre_delete` - Callback for pre-delete of upload
* `FlaskTus.post_delete` - Callback for post-delete of upload


## Extending

## Extension
The extension can be extended in terms of callbacks, custom methods etc. as in the following example

```python 
from flask_tus import FlaskTus

class FlaskTusExtended(FlaskTus):
    def on_complete(self):
        print('Succesful upload')
```

For the model, "MongoengineUpload", MD5 can be calculated and set for the upload by accesing the property `MD5` which could be done on the `flask_tus.on_completion` method, but should be done on by a task in production.

## Custom models
Custom models and features can be added by suppling a custom repository in the instantiation of the extensions object.

# CLI

The extensions supports deletion of expired downsload by the CLI-command

```bash
$ tus delete_expired
```

Which can be scheduled with eg. `cron`.
