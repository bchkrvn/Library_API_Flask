from dao.models.models_dao import Comment


class CommentDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(Comment).all()

    def get_one(self, c_id):
        return self.session.query(Comment).get(c_id)

    def get_by_news_id(self, n_id):
        return self.session.query(Comment).filter(Comment.news_id == n_id).all()

    def save(self, comment):
        self.session.add(comment)
        self.session.commit()

    def delete(self, comment):
        self.session.delete(comment)
        self.session.commit()

    def delete_by_news_id(self, n_id):
        self.session.query(Comment).filter(Comment.news_id == n_id).delete()
        self.session.commit()
