from ..extensions.db import db


class BaseRepository:

    def __init__(self, model):
        self.model = model

    def get_by_id(self, id_):
        return self.model.query.get(id_)

    def list_all(self):
        return self.model.query.all()

    def add(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()

    def save_changes(self):
        db.session.commit()

    def refresh(self, entity):
        db.session.refresh(entity)
        return entity