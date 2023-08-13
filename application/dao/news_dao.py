from dao import BaseDAO
from models import News


class NewsDAO(BaseDAO):
    """
    DAO для работы с новостями
    """
    __model__ = News
