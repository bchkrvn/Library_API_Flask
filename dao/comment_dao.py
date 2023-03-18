from dao.base_dao import BaseDAO
from dao.models.models_dao import Comment


class CommentDAO(BaseDAO):
    __model__ = Comment

    def __init__(self, session):
        super().__init__(session=session)

    def get_by_news_id(self, n_id):
        return self._session.query(self.__model__).filter(self.__model__.news_id == n_id).all()

    def delete_by_news_id(self, n_id):
        self._session.query(self.__model__).filter(self.__model__.news_id == n_id).delete()
        self._session.commit()
