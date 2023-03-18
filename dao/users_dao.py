from dao.base_dao import BaseDAO
from dao.models.models_dao import User


class UserDAO(BaseDAO):
    __model__ = User

    def __init__(self, session):
        super().__init__(session=session)

    def get_by_name(self, name):
        return self._session.query(User).filter(User.username == name).first()

