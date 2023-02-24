import pytest

from dao.models_dao import Author
from services.authors_service import AuthorService


class TestAuthorService:
    @pytest.fixture(autouse=True)
    def author_service(self, author_dao):
        self.author_service = AuthorService(author_dao)

    def test_get_one_author(self):
        author = self.author_service.get_one(1)

        assert author is not None, 'Вместо автора возвращается None'
        assert type(author) is Author, 'Возвращается на автор'
        assert type(author.id) is int, 'id автора не число'
        assert type(author.first_name) is str, 'Имя автора не строка'
        assert type(author.middle_name) is str, 'Отчества автора не строка'
        assert type(author.last_name) is str, 'Фамилия автора не строка'

    def test_get_all_authors(self):
        authors = self.author_service.get_all()

        assert authors is not None, 'Возвращается None вместо авторов'
        assert type(authors) is list, 'Возвращается не список'
        assert type(authors[0]) is Author, 'Элементы списка не авторы'

