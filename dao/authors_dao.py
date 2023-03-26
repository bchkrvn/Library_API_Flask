from dao.base_dao import BaseDAO
from dao.models.models_dao import Author


class AuthorDAO(BaseDAO):
    __model__ = Author

    def __init__(self, session):
        super().__init__(session=session)

    def get_by_name(self, first_name, last_name):
        return self._session.query(self.__model__).filter(self.__model__.first_name == first_name,
                                                          self.__model__.last_name == last_name).first()
