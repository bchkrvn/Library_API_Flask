from application.dao.models.models_dao import Author


class TestAuthorDAO:
    def test_get_all(self, author_1, author_2, author_dao):
        authors = author_dao.get_all()

        assert authors is not None, "Возвращается None вместо авторов"
        assert type(authors) is list, 'Возвращается не список'
        assert len(authors) == 2, f'Возвращается больше авторов({len(authors)}), чем ожидалось(2)'
        assert author_1 in authors, "Первого автора нет в списке"
        assert author_2 in authors, "Второго автора нет в списке"

    def test_get_one(self, author_1, author_dao):
        author = author_dao.get_one(author_1.id)

        assert author is not None, "Возвращается None вместо автора"
        assert type(author) is Author, f'Возвращается не автор, а {type(author)}'
        assert author.id == author_1.id, "id автора не совпадает"
        assert author.first_name == author_1.first_name, "first_name автора не совпадают"
        assert author.middle_name == author_1.middle_name, "middle_name автора не совпадают"
        assert author.last_name == author_1.last_name, "last_name автора не совпадают"

        # Несуществующий автор
        author_2 = author_dao.get_one(2)
        assert author_2 is None, f'Возвращается {type(author_2)}, вместо None'

    def test_get_by_name(self, author_1, author_dao):
        author = author_dao.get_by_name(author_1.first_name, author_1.last_name)

        assert author is not None, "Возвращается None вместо автора"
        assert type(author) is Author, f'Возвращается не автор, а {type(author)}'
        assert author.id == author_1.id, "id автора не совпадает"
        assert author.first_name == author_1.first_name, "first_name автора не совпадают"
        assert author.middle_name == author_1.middle_name, "middle_name автора не совпадают"
        assert author.last_name == author_1.last_name, "last_name автора не совпадают"

        # Несуществующий автор
        author_2 = author_dao.get_by_name('Wrong_name', author_1.last_name)
        assert author_2 is None, f'Возвращается {type(author_2)}, вместо None'
        author_3 = author_dao.get_by_name(author_1.first_name, 'wrong_last_name')
        assert author_3 is None, f'Возвращается {type(author_3)}, вместо None'

    def test_save(self, author_dao):
        new_author = Author(first_name='Имя', middle_name="Отчество", last_name="Фамилия")
        author_dao.save(new_author)
        author = author_dao.get_all()[-1]

        assert author is not None, "Возвращается None вместо автора"
        assert type(author) is Author, f'Возвращается не автор, а {type(author)}'
        assert author.id == new_author.id, "id автора не совпадает"
        assert author.first_name == new_author.first_name, "first_name автора не совпадают"
        assert author.middle_name == new_author.middle_name, "middle_name автора не совпадают"
        assert author.last_name == new_author.last_name, "last_name автора не совпадают"

    def test_delete(self, author_1, author_dao):
        author_dao.delete(author_1)
        authors = author_dao.get_all()

        assert len(authors) == 0, "Автор не удалился"
