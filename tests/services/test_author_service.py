import pytest
from werkzeug.exceptions import NotFound

from app.dao.models.models_dao import Author


class TestAuthorService:
    def test_get_all(self, author_1, author_2, author_service):
        authors = author_service.get_all()

        assert authors is not None, "Возвращается None вместо авторов"
        assert type(authors) is list, 'Возвращается не список'
        assert len(authors) == 2, f'Возвращается больше авторов({len(authors)}), чем ожидалось(2)'
        assert author_1 in authors, "Первого автора нет в списке"
        assert author_2 in authors, "Второго автора нет в списке"

    def test_get_one(self, author_1, author_service):
        author = author_service.get_one(author_1.id)

        assert author is not None, "Возвращается None вместо автора"
        assert type(author) is Author, f'Возвращается не автор, а {type(author)}'
        assert author.id == author_1.id, "id автора не совпадает"
        assert author.first_name == author_1.first_name, "first_name автора не совпадают"
        assert author.middle_name == author_1.middle_name, "middle_name автора не совпадают"
        assert author.last_name == author_1.last_name, "last_name автора не совпадают"

        with pytest.raises(NotFound):
            author = author_service.get_one(2)

    def test_get_by_name(self, author_1, author_service):
        author = author_service.get_by_name(author_1.first_name, author_1.last_name)

        assert author is not None, "Возвращается None вместо автора"
        assert type(author) is Author, f'Возвращается не автор, а {type(author)}'
        assert author.id == author_1.id, "id автора не совпадает"
        assert author.first_name == author_1.first_name, "first_name автора не совпадают"
        assert author.middle_name == author_1.middle_name, "middle_name автора не совпадают"
        assert author.last_name == author_1.last_name, "last_name автора не совпадают"

        # Несуществующий автор
        with pytest.raises(NotFound):
            author_2 = author_service.get_by_name('Wrong_name', author_1.last_name)
        with pytest.raises(NotFound):
            author_3 = author_service.get_by_name(author_1.first_name, 'wrong_last_name')

    def test_create(self, author_service):
        data = {
            'first_name': 'first_name',
            'middle_name': 'middle_name',
            'last_name': 'last_name',
        }
        author_service.create(data)
        author = author_service.get_one(1)

        assert author is not None, "Возвращается None вместо автора"
        assert type(author) is Author, f'Возвращается не автор, а {type(author)}'
        assert author.id == 1, "id автора не совпадает"
        assert author.first_name == data.get('first_name'), "first_name автора не совпадают"
        assert author.middle_name == data.get('middle_name'), "middle_name автора не совпадают"
        assert author.last_name == data.get('last_name'), "last_name автора не совпадают"

    def test_update(self, author_1, author_service):
        data = {
            'id': 1,
            'first_name': 'first_name',
            'middle_name': 'middle_name',
            'last_name': 'last_name',
        }
        author_service.update(data)
        author = author_service.get_one(1)

        assert author is not None, "Возвращается None вместо автора"
        assert type(author) is Author, f'Возвращается не автор, а {type(author)}'
        assert author.id == 1, "id автора не совпадает"
        assert author.first_name == data.get('first_name'), "first_name автора не совпадают"
        assert author.middle_name == data.get('middle_name'), "middle_name автора не совпадают"
        assert author.last_name == data.get('last_name'), "last_name автора не совпадают"

        with pytest.raises(NotFound):
            data['id'] = 2
            author = author_service.update(data)

    def test_update_partial(self, author_1, author_service):
        data = {
            'id': 1,
            'first_name': 'first_name',
            'middle_name': 'middle_name',
            'last_name': 'last_name',
        }
        author_service.update_partial(data)
        author = author_service.get_one(1)

        assert author is not None, "Возвращается None вместо автора"
        assert type(author) is Author, f'Возвращается не автор, а {type(author)}'
        assert author.id == 1, "id автора не совпадает"
        assert author.first_name == data.get('first_name'), "first_name автора не совпадают"
        assert author.middle_name == data.get('middle_name'), "middle_name автора не совпадают"
        assert author.last_name == data.get('last_name'), "last_name автора не совпадают"

        with pytest.raises(NotFound):
            data['id'] = 2
            author = author_service.update(data)

    def test_delete(self, author_1, author_service):
        author_service.delete(author_1.id)
        authors = author_service.get_all()

        assert len(authors) == 0, 'Автор не удален'

        with pytest.raises(NotFound):
            author_service.delete(1)
