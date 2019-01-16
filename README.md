# flask-tus
[tus](https://www.tus.io) server implementation for [Flask](https://flask.pocoo.org).

# Requirements
Following software stack is required to run this project:
* [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/)
* [python3](https://www.python.org/)
* [pip3]()
* [pipenv](https://pipenv.readthedocs.io/en/latest/) or [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

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
$ ./setup.py install
```

### docker
```bash
$ git clone https://github.com/volesen/flask-tus.git
$ cd flask-tus
$ docker-compose -f docker-compose.yml up
```


### Running a demo project
```bash
$ python demo/app.py
```
Go to [127.0.0.1:5000](http://127.0.0.1:5000) and upload a file. The uploaded file will end in `demo/uploads/`

### Testing project
```bash
$ pytest -v tests/
```
# Usage
## Settings
Settings are added in app.config:
* `TUS_UPLOAD_URL` - Url of endpoint
* `TUS_UPLOAD_DIR` - Path to upload directory. Can be changed with custom models (eg. for saving in AWS S3)
* `TUS_MAX_SIZE` - Max size of a file-upload
* `TUS_TIMEDELTA` - Time allowed to complete upload

## Models
Upload states are by default saved in memory, but can be saved persistently, as in the following example:

```python
from flask import Flask
from flask_tus import FlaskTus
from flask_tus.models import MongoengineUpload

def create_app(config):
  app = Flask(__name__)  
  app.config.from_object(config)

  flask_tus = FlaskTus(model=MongoengineUpload)
  flask_tus.init_app()

  return app
```
For the MongoDB model, the collection will be named
> uploads

## Extending
The extensions can be extending in terms of callbacks and model, as in the following examples
```python 
from flask_tus import FlaskTus


class FlaskTusExtended(FlaskTus):
    def on_complete(self):
        print('Succesful upload')
```

The callbacks are as follows:
* `FlaskTus.on_create` - Callback for creation of upload
* `FlaskTus.pre_save` - Callback for pre-save on each chunk
* `FlaskTus.post_save` - Callback for post-save on each chunk
* `FlaskTus.on_complete` - Callback for completion of upload
* `FlaskTus.pre_delete` - Callback for pre-delete of upload
* `FlaskTus.post_delete` - Callback for post-delete of upload

For the model, "MongoengineUpload", MD5 can be calculated and set for the upload by accesing the property `MD5`

Model can be extended by inheriting the base models:
```python 
from flask_tus.models import MongoengineUpload
from mongoengine import StringField

class CustomModel(MongoengineUpload)
  owner = StringField()
    
  @classmethod
  def create(cls, upload_length, metadata, owner):
      """ Factory method"""
      return cls(length=upload_length, metadata=metadata, owner = owner)
```

