from ..dao.models.models_dao import Reader, User
from ..dao.readers_dao import ReaderDAO
from flask import abort


class ReaderService:
    """
    Сервис для работы с читателем
    """
    def __init__(self, dao: ReaderDAO):
        self.dao = dao

    def get_all(self) -> list[Reader]:
        """
        Получить всех читателей
        :return: list[Reader]
        """
        return self.dao.get_all()

    def get_one(self, id_: int) -> Reader:
        """
        Получить читателя по его id
        :param id_: id читателя
        :return: Reader
        """
        reader = self.dao.get_one(id_)
        if not reader:
            abort(404, f'reader with id={id_} not found')
        return reader

    def create(self, user: User):
        """
        Создание нового читателя при создании нового пользователя
        :param user: новый пользователь
        """
        new_reader = Reader(
            first_name=None,
            last_name=None,
            user=user
        )
        self.dao.save(new_reader)

    def update(self, data: dict):
        """
        Обновить информацию о пользователе
        :param data: данные, содержащие id, имя и фамилию
        """
        reader = self.get_one(data.get('id'))
        reader.first_name = data.get('first_name')
        reader.last_name = data.get('last_name')
        self.dao.save(reader)

    def update_partial(self, data: dict):
        """
        Частично обновить информацию о пользователе
        :param data: данные, содержащие id а также имя или фамилию
        """
        id_ = data.get('id')
        reader = self.get_one(id_)

        if 'first_name' in data:
            reader.first_name = data.get('first_name')
        if 'last_name' in data:
            reader.last_name = data.get('last_name')

        self.dao.save(reader)

    def delete(self, id_: int):
        """
        Удалить читателя при удалении пользователя
        :param id_: id читателя
        """
        reader = self.get_one(id_)
        self.dao.delete(reader)

