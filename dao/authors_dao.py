from dao.models.models_dao import Author


class AuthorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Author).all()

    def get_one(self, id_):
        return self.session.query(Author).get(id_)

    def save(self, author):
        self.session.add(author)
        self.session.commit()

    def delete(self, author):
        self.session.delete(author)
        self.session.commit()
