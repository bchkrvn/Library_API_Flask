from application.dao.base_dao import BaseDAO
from application.dao.models.models_dao import Reader


class ReaderDAO(BaseDAO):
    """
    DAO для работы с читателями
    """
    __model__ = Reader

    def __init__(self, session):
        super().__init__(session=session)
