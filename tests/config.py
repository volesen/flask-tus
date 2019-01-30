import tempfile
import datetime
import mongoengine

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from flask_tus.models import (
    MongoengineBaseUpload,
    MongoengineUpload)
from flask_tus.models.sqlalchemy_model import Base, SQLAlchemyModel


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy


class BaseTestConfig:
    TESTING = True
    TUS_UPLOAD_DIR = tempfile.mkdtemp()
    TUS_UPLOAD_VIEW = '/files/'
    TUS_MAX_SIZE = 2 ** 32
    TUS_TIMEDELTA = datetime.timedelta(days=1)


class MongoengineBaseUploadConfig(BaseTestConfig):
    model = MongoengineBaseUpload

    def init_db(app= None):
        mongoengine.connect('test', host='mongodb', port=27017)


class MongoengineUploadConfig(MongoengineBaseUploadConfig):
    model = MongoengineUpload


class SQLAlchemyModelConfig(BaseTestConfig):
    model = SQLAlchemyModel
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    @staticmethod
    def init_db(app):
        db = SQLAlchemy(app)
        Base.metadata.drop_all(bind=db.engine)
        Base.metadata.create_all(bind=db.engine)
        return db
