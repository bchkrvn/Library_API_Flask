from dao.base_dao import BaseDAO
from dao.models.models_dao import News


class NewsDAO(BaseDAO):
    """
    DAO для работы с новостями
    """
    __model__ = News
