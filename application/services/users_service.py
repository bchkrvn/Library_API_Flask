from sqlalchemy.exc import IntegrityError
from flask import abort

from models import User
from dao import UserDAO
from services.books_service import BookService
from services.readers_service import ReaderService
from tools import get_hash, compare_password


class UserService:
    """
    Сервис для работы с пользователями
    """

    def __init__(self, dao: UserDAO, reader_service: ReaderService, books_service: BookService):
        self.dao = dao
        self.reader_service = reader_service
        self.books_service = books_service

    def get_all(self) -> list[User]:
        """
        Получить всех пользователей
        :return: list[User]
        """
        return self.dao.get_all()

    def get_one(self, id_: int) -> User:
        """
        Получить пользователя по его id
        :param id_: id пользователя
        :return: User
        """
        user = self.dao.get_one(id_)
        if not user:
            abort(404, f'User with id={id_} not found')
        return user

    def get_by_username(self, username: str) -> User:
        """
        Получить пользователя по его никнейму
        :param username: никнейм пользователя
        :return: User
        """
        user = self.dao.get_by_name(username)
        if not user:
            abort(404, f"User '{username}' not found")
        return user

    def create(self, data: dict):
        """
        Создание нового пользователя
        :param data: данные, содержащие никнейм и пароль
        """
        data['role'] = 'user'
        data['password'] = get_hash(data['password'])
        user = User(**data)
        try:
            self.dao.save(user)
        except IntegrityError:
            abort(400, 'username is not unique')
        self.reader_service.create(user)

    def update(self, data: dict):
        """
        Обновить никнейм пользователя
        :param data: словарь с новым никнеймом
        """
        user = self.get_one(data['id'])
        user.username = data.get('username')
        try:
            self.dao.save(user)
        except IntegrityError:
            abort(400, 'username is not unique')

    def delete(self, id_: int):
        """
        Удалить пользователя по его id
        :param id_: id пользователя
        """
        user = self.get_one(id_)
        books = self.books_service.filter_books(reader_id=user.id)
        if books:
            return abort(400, 'Reader have books')

        self.dao.delete(user)
        self.reader_service.delete(id_)

    def change_password(self, data: dict):
        """
        Обновить пароль пользователя
        :param data: данные, содержащие id пользователя, старый и новый пароль
        """
        user = self.get_one(data['user_id'])

        if compare_password(user.password, data['old_password']):
            new_password = data.get('new_password')
            user.password = get_hash(new_password)
            self.dao.save(user)
        else:
            abort(400, 'Wrong password')
