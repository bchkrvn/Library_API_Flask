from dao import BaseDAO
from models import Book


class BookDAO(BaseDAO):
    """
    DAO для книг
    """
    __model__ = Book

    def get_all(self, result=None) -> list[Book]:
        """
        Получить все книги из БД сразу или после фильтрации
        :param result: результат фильтрации
        :return: list[Book]
        """
        if result:
            return result.all()
        return self._session.query(self.__model__).all()

    def get_all_to_filter(self):
        """
        Создание запроса для фильтрации
        """
        return self._session.query(self.__model__)

    def get_by_author(self, request, author_id: int):
        """
        Добавление фильтра по автору
        :param request: запрос
        :param author_id: id автора
        """
        return request.filter(self.__model__.author_id == author_id)

    def get_by_reader(self, request, reader_id: int):
        """
        Добавление фильтра по читателю
        :param request: запрос
        :param reader_id: id читателя
        :return:
        """
        return request.filter(self.__model__.reader_id == reader_id)

    def get_by_available(self, request, choice: bool):
        """
        Фильтрация по наличию
        :param request: запрос
        :param choice: True or False
        """
        return request.filter(self.__model__.is_in_lib == choice)
