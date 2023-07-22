from application.dao.base_dao import BaseDAO
from application.dao.models.models_dao import Author


class AuthorDAO(BaseDAO):
    """
    DAO для авторов
    """
    __model__ = Author

    def __init__(self, session):
        super().__init__(session=session)

    def get_by_name(self, first_name: str, last_name: str) -> list[Author]:
        """
        Получить авторов из БД по имени и фамилии
        :param first_name: имя
        :param last_name: фамилия
        :return: list[Authors]
        """
        return self._session.query(self.__model__).filter(self.__model__.first_name == first_name,
                                                          self.__model__.last_name == last_name).first()
