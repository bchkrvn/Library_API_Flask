from dao.models.models_dao import Reader


class ReaderDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Reader).all()

    def get_one(self, id_):
        return self.session.query(Reader).get(id_)

    def save(self, reader: Reader):
        self.session.add(reader)
        self.session.commit()

    def delete(self, reader: Reader):
        self.session.delete(reader)
        self.session.commit()
