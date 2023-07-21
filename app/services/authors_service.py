from flask import abort
from app.dao.authors_dao import AuthorDAO
from app.dao.models.models_dao import Author


class AuthorService:
    """
    Сервис для работы с авторами
    """
    def __init__(self, dao: AuthorDAO):
        self.dao = dao

    def get_all(self) -> list[Author]:
        """
        Получить всех авторов
        :return: Список авторов
        """
        return self.dao.get_all()

    def get_one(self, id_: int) -> Author:
        """
        Получить одного автора по его id
        :param id_: id автора
        :return: автор
        """
        author = self.dao.get_one(id_)
        if not author:
            abort(404, f'author with id={id_} not found')
        return author

    def get_by_name(self, first_name: str, last_name: str) -> Author:
        """
        Получить одного автора по его имени и фамилии
        :param first_name: имя
        :param last_name: фамилия
        :return: автор
        """
        author = self.dao.get_by_name(first_name, last_name)
        if not author:
            abort(404, f'author "{first_name} {last_name}" not found')
        return author

    def create(self, data: dict) -> None:
        """
        Добавить нового автора в БД
        :param data: Данные, содержащие Имя, Фамилию и Отчество
        """
        new_author = Author(**data)
        self.dao.save(new_author)

    def update(self, data: dict) -> None:
        """
        Обновить данные у автора
        :param data: Данные, содержащие Имя, Фамилию и Отчество
        :return:
        """
        author = self.get_one(data['id'])
        author.first_name = data.get('first_name')
        author.middle_name = data.get('middle_name')
        author.last_name = data.get('last_name')
        self.dao.save(author)

    def update_partial(self, data: dict) -> None:
        """
        Частично обновить данные у автора
        :param data: Данные, которые могут содержать Имя, Фамилию и Отчество
        """
        author = self.get_one(data['id'])
        if 'first_name' in data:
            author.first_name = data.get('first_name')
        if 'middle_name' in data:
            author.middle_name = data.get('middle_name')
        if 'last_name' in data:
            author.last_name = data.get('last_name')
        self.dao.save(author)

    def delete(self, id_: int) -> None:
        """
        Удалить автора по его id
        :param id_: id автора
        """
        author = self.get_one(id_)
        self.dao.delete(author)
