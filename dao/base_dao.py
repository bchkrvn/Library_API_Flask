class BaseDAO:
    __model__ = None

    def __init__(self, session):
        self._session = session

    def get_all(self):
        return self._session.query(self.__model__).all()

    def get_one(self, id_):
        return self._session.query(self.__model__).get(id_)

    def save(self, object_):
        self._session.add(object_)
        self._session.commit()

    def delete(self, object_):
        self._session.delete(object_)
        self._session.commit()
