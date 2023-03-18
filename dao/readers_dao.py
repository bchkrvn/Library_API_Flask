from dao.base_dao import BaseDAO
from dao.models.models_dao import Reader


class ReaderDAO(BaseDAO):
    __model__ = Reader

    def __init__(self, session):
        super().__init__(session=session)
