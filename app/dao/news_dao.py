from app.dao.base_dao import BaseDAO
from app.dao.models.models_dao import News


class NewsDAO(BaseDAO):
    """
    DAO для работы с новостями
    """
    __model__ = News

    def __init__(self, session):
        super().__init__(session=session)
