from dao.base_dao import BaseDAO
from dao.models.models_dao import News


class NewsDAO(BaseDAO):
    __model__ = News

    def __init__(self, session):
        super().__init__(session=session)
