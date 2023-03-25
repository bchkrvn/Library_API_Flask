from sqlalchemy.exc import IntegrityError

from flask import abort
from dao.models.models_dao import User
from dao.users_dao import UserDAO
from services.readers_service import ReaderService
from tools.security import get_hash, compare_password


class UserService:
    def __init__(self, dao: UserDAO, reader_service: ReaderService):
        self.dao = dao
        self.reader_service = reader_service

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, id_):
        user = self.dao.get_one(id_)
        if not user:
            abort(404, f'User with id={id_} not found')
        return user

    def get_by_username(self, username):
        user = self.dao.get_by_name(username)
        if not user:
            abort(404, f'User "{username}" not found')
        return user

    def create(self, data):
        data['role'] = 'user'
        data['password'] = get_hash(data['password'])
        user = User(**data)
        try:
            self.dao.save(user)
        except IntegrityError:
            abort(400, 'username is not unique')
        self.reader_service.create(user)

    def update(self, data):
        user = self.get_one(data['id'])
        user.username = data.get('username')
        try:
            self.dao.save(user)
        except IntegrityError:
            abort(400, 'username is not unique')

    def delete(self, id_):
        user = self.get_one(id_)
        self.dao.delete(user)
        self.reader_service.delete(id_)

    def change_password(self, data):
        user = self.get_one(data['user_id'])

        if compare_password(user.password, data['old_password']):
            new_password = data.get('new_password')
            user.password = get_hash(new_password)
            self.dao.save(user)
        else:
            abort(400, 'Wrong password')
