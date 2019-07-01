import datetime

from flask import current_app
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from .base_repository import BaseRepository
from ..exceptions import TusError


class SQLRepository(BaseRepository):

    def __init__(self, model, db):
        super(SQLRepository, self).__init__(model, db)

    def create(self, *args, **kwargs):
        # The field 'metadata' is reserved in SQLAlchemy therefore _metadata is used
        metadata = kwargs.get('metata')
        del kwargs['metadata']

        # Instantiate model
        instance = self.model(_metadata=metadata, **kwargs)

        # Add and commit model to db
        self.db.session.add(instance)
        self.db.session.commit()

        return instance

    def find_by(self, **kwargs):
        return self.db.session.query(self.model).filter(**kwargs)

    def find_by_id(self, uuid):
        """ Finds upload by upload_uuid """
        try:
            return self.db.session.query(self.model).filter(self.model.upload_uuid == uuid).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            raise TusError(500, 'upload_uuid not unique')

    def delete_expired(self):
        # Get expired uploads
        query = self.db.session.query(self.model).filter(
            self.model.created_on <= datetime.datetime.now() - current_app.config['TUS_EXPIRATION'])

        # Delete expired uploads
        query.delete()
        self.db.session.commit()
