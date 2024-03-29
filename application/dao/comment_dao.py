from dao import BaseDAO
from models import Comment


class CommentDAO(BaseDAO):
    """
    DAO для работы с комментариями
    """
    __model__ = Comment

    def get_by_news_id(self, n_id: int) -> list[Comment]:
        """
        Получить комментарии по id новости из БД
        :param n_id: id новости
        :return: list[Comment}
        """
        return self._session.query(self.__model__).filter(self.__model__.news_id == n_id).all()

    def delete_by_news_id(self, n_id: int):
        """
        Удалить комментарии по id новости
        :param n_id: id новости
        """
        self._session.query(self.__model__).filter(self.__model__.news_id == n_id).delete()
        self._session.commit()
