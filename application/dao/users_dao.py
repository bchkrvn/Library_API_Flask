from dao.base_dao import BaseDAO
from dao.models.models_dao import User


class UserDAO(BaseDAO):
    """
    DAO для работы с пользователями
    """
    __model__ = User

    def get_by_name(self, username: str) -> User:
        """
        Получить пользователя из БД по его никнейму
        :param username: никнейм пользователя
        :return: User
        """
        return self._session.query(self.__model__).filter(self.__model__.username == username).first()
