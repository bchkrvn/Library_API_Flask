from dao.models.models_dao import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_one(self, id_):
        return self.session.query(User).get(id_)

    def get_by_name(self, name):
        return self.session.query(User).filter(User.username == name).first()

    def save(self, user: User):
        self.session.add(user)
        self.session.commit()

    def delete(self, id_):
        user = self.get_one(id_)
        self.session.delete(user)
        self.session.commit()
