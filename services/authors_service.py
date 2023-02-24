from flask import abort
from dao.authors_dao import AuthorDAO
from dao.models.models_dao import Author


class AuthorService:
    def __init__(self, dao: AuthorDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, id_):
        book = self.dao.get_one(id_)
        if not book:
            abort(404, f'author with id={id_} not found')
        return book

    def create(self, data):
        new_author = Author(**data)
        self.dao.save(new_author)

    def update(self, data):
        author = self.get_one(data['id'])
        author.first_name = data.get('first_name')
        author.middle_name = data.get('middle_name')
        author.last_name = data.get('last_name')
        self.dao.save(author)

    def update_partial(self, data):
        author = self.get_one(data['id'])
        if 'first_name' in data:
            author.first_name = data.get('first_name')
        if 'middle_name' in data:
            author.middle_name = data.get('middle_name')
        if 'last_name' in data:
            author.last_name = data.get('last_name')
        self.dao.save(author)

    def delete(self, id_):
        author = self.get_one(id_)
        self.dao.delete(author)
