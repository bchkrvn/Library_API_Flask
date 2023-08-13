from dao import BaseDAO
from models import Author


class AuthorDAO(BaseDAO):
    """
    DAO для авторов
    """
    __model__ = Author

    def get_by_name(self, first_name: str, last_name: str) -> list[Author]:
        """
        Получить авторов из БД по имени и фамилии
        :param first_name: имя
        :param last_name: фамилия
        :return: list[Authors]
        """
        return self._session.query(self.__model__).filter(self.__model__.first_name == first_name,
                                                          self.__model__.last_name == last_name).first()
