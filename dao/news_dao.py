from dao.models.models_dao import News


class NewsDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(News).all()

    def get_one(self, n_id):
        return self.session.query(News).get(n_id)

    def save(self, news):
        self.session.add(news)
        self.session.commit()

    def delete(self, news):
        self.session.delete(news)
        self.session.commit()
