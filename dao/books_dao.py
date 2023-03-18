from dao.base_dao import BaseDAO
from dao.models.models_dao import Book


class BookDAO(BaseDAO):
    __model__ = Book

    def __init__(self, session):
        super().__init__(session=session)

    def get_all(self, result=None):
        if result:
            return result.all()
        return self._session.query(self.__model__).all()

    def get_all_to_filter(self):
        return self._session.query(self.__model__)

    def get_by_author(self, request, author_id):
        return request.filter(self.__model__.author_id == author_id)

    def get_by_reader(self, request, reader_id):
        return request.filter(self.__model__.reader_id == reader_id)

    def get_by_available(self, request, choice):
        return request.filter(self.__model__.is_in_lib == choice)
