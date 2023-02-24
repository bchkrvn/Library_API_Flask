from dao.models.models_dao import Book


class BookDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self, result=None):
        if result:
            return result.all()
        else:
            return self.session.query(Book).all()

    def get_all_to_filter(self):
        return self.session.query(Book)

    def get_one(self, id_):
        return self.session.query(Book).get(id_)

    def get_by_author(self, request, author_id):
        return request.filter(Book.author_id == author_id)

    def get_by_reader(self, request, reader_id):
        return request.filter(Book.reader_id == reader_id)

    def get_by_available(self, request, choice):
        return request.filter(Book.is_in_lib == choice)

    def save(self, book: Book):
        self.session.add(book)
        self.session.commit()

    def delete(self, book: Book):
        self.session.delete(book)
        self.session.commit()
