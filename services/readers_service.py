from dao.models.models_dao import Reader
from dao.readers_dao import ReaderDAO
from flask import abort


class ReaderService:
    def __init__(self, dao: ReaderDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, id_):
        reader = self.dao.get_one(id_)
        if not reader:
            abort(404, f'reader with id={id_} not found')
        return reader

    def create(self, user):
        new_reader = Reader(
            first_name=None,
            last_name=None,
            user=user
        )
        self.dao.save(new_reader)

    def update(self, data):
        reader = self.get_one(data.get('id'))

        reader.first_name = data.get('first_name')
        reader.last_name = data.get('last_name')

        self.dao.save(reader)

    def update_partial(self, data):
        id_ = data.get('id')
        reader = self.get_one(id_)

        if 'first_name' in data:
            reader.first_name = data.get('first_name')
        if 'last_name' in data:
            reader.last_name = data.get('last_name')

        self.dao.save(reader)

    def delete(self, id_):
        reader = self.get_one(id_)
        self.dao.delete(reader)

