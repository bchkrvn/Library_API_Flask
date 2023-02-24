import base64
import hashlib
import hmac
from flask import abort

from constants import JWT_ALGO, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.models.models_dao import User
from dao.users_dao import UserDAO
from services.readers_service import ReaderService


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
        if 'role' not in data:
            data['role'] = 'user'
        data['password'] = self.get_hash(data['password'])
        user = User(**data)
        self.dao.save(user)
        self.reader_service.create(user)

    def update(self, data):
        user = self.get_one(data['id'])

        user.username = data.get('username')
        user.password = self.get_hash(data['password'])
        user.role = data.get('role')
        self.dao.save(user)

    def update_partial(self, data):
        user = self.get_one(data['id'])

        if 'username' in data:
            user.username = data.get('username')
        if 'password' in data:
            user.password = self.get_hash(data['password'])
        if 'role' in data:
            user.role = data.get('role')
        self.dao.save(user)

    def delete(self, id_):
        self.dao.delete(id_)
        self.reader_service.delete(id_)

    def get_hash(self, password):
        hash_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_password)

    def compare_password(self, right_password, other_password) -> bool:
        decode_right_password = base64.b64decode(right_password)
        hash_other_password = hashlib.pbkdf2_hmac(
            JWT_ALGO,
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decode_right_password, hash_other_password)
