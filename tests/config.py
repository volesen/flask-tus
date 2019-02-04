import tempfile
import datetime
import mongoengine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

from flask_tus.models import MongoengineBaseModel, MongoengineModel, SQLAlchemyModel
from flask_tus.models.sqlalchemy_model import Base


class BaseTestConfig:
    TESTING = True
    TUS_UPLOAD_DIR = tempfile.mkdtemp()
    TUS_UPLOAD_VIEW = '/files/'
    TUS_MAX_SIZE = 2 ** 32
    TUS_EXPIRATION = datetime.timedelta(days=1)


class MongoengineBaseUploadConfig(BaseTestConfig):
    model = MongoengineBaseModel

    @staticmethod
    def init_db(app):
        mongoengine.connect('test', host='mongodb', port=27017)


class MongoengineUploadConfig(MongoengineBaseUploadConfig):
    model = MongoengineModel


class SQLAlchemyModelConfig(BaseTestConfig):
    model = SQLAlchemyModel
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_db(app):
        # Instantiate DB object
        db = SQLAlchemy(app)

        # Create new tables
        Base.metadata.drop_all(bind=db.engine)
        Base.metadata.create_all(bind=db.engine)
        
        return db
