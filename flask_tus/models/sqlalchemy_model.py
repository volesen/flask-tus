import uuid
import datetime

from flask import current_app
from sqlalchemy import Column, Integer, String, DateTime, PickleType, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from .base_model import BaseTusModel
from ..storage.file_wrapper import FileWrapper
from ..exceptions import TusError

Base = declarative_base()


def get_uuid():
    return str(uuid.uuid4())


class SQLAlchemyModel(Base, BaseTusModel):
    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True)
    upload_uuid = Column(String(36), default=get_uuid, unique=True, nullable=False)
    filename = Column(String(255))
    path = Column(String(255), nullable=False)
    length = Column(Integer)
    offset = Column(Integer, default=0, nullable=False)
    _metadata = Column(PickleType)  # "metadata" is protected
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)

    @property
    def file(self):
        return FileWrapper(self.path)

    @property
    def expires(self):
        return self.created_on + current_app.config['TUS_EXPIRATION']

    @property
    def expired(self):
        return datetime.datetime.now() > self.expires

    def append_chunk(self, chunk):
        # Handle file and increment offset on every append
        current_app.flask_tus.pre_save()
        try:
            FileWrapper(self.path).append_chunk(chunk)
        except OSError:
            raise TusError(503)
        else:
            # Increment offset
            self.offset += len(chunk)
            current_app.flask_tus.repo.db.session.commit()
            current_app.flask_tus.post_save()

    def delete(self):
        # On unsuccessful deletion raise "500 Internal Server Error"
        current_app.flask_tus.pre_delete()
        try:
            FileWrapper(self.path).delete()
        except OSError:
            raise TusError(500)
        else:
            current_app.flask_tus.repo.db.session.delete(self)
            current_app.flask_tus.repo.db.session.commit()
            current_app.flask_tus.post_delete()
