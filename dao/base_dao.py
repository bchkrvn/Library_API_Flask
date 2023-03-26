class BaseDAO:
    """
    Базовый класс DAO
    """
    __model__ = None

    def __init__(self, session):
        self._session = session

    def get_all(self) -> list[object]:
        """
        Получить все объекты
        :return: list[object]
        """
        return self._session.query(self.__model__).all()

    def get_one(self, id_: int) -> object:
        """
        Получить объект по его id
        :param id_: id объекта
        :return: object
        """
        return self._session.query(self.__model__).get(id_)

    def save(self, object_: object):
        """
        Сохранить объект в БД
        """
        self._session.add(object_)
        self._session.commit()

    def delete(self, object_: object):
        """
        Удалить объект из БД
        """
        self._session.delete(object_)
        self._session.commit()
