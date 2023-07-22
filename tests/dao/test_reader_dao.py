from dao.models.models_dao import Reader


class TestReaderDAO:
    def test_get_all(self, reader_1, reader_2, reader_dao):
        readers = reader_dao.get_all()

        assert readers is not None, "Возвращается None вместо читателей"
        assert type(readers) is list, 'Возвращается не список'
        assert len(readers) == 2, f'Возвращается больше читателей({len(readers)}), чем ожидалось(2)'
        assert reader_1 in readers, "Первого читателя нет в списке"
        assert reader_2 in readers, "Второго читателя нет в списке"

    def test_get_one(self, reader_1, reader_dao):
        reader = reader_dao.get_one(reader_1.id)

        assert reader is not None, "Возвращается None вместо читателя"
        assert type(reader) is Reader, f'Возвращается не читатель, а {type(reader)}'
        assert reader.id == reader_1.id, "id читателя не совпадает"
        assert reader.first_name == reader_1.first_name, "first_name читателя не совпадает"
        assert reader.last_name == reader_1.last_name, "last_name читателя не совпадает"
        assert reader.user_id == reader_1.user_id, "user_id читателя не совпадает"

        reader_2 = reader_dao.get_one(2)

        assert reader_2 is None, f'Возвращается {type(reader)} вместо None'

    def test_save(self, reader_dao):
        r = Reader(
            first_name='Имя_1',
            last_name='Фамилия_1',
            user_id=1
        )
        reader_dao.save(r)
        reader = reader_dao.get_one(r.id)

        assert reader is not None, "Возвращается None вместо читателя"
        assert type(reader) is Reader, f'Возвращается не читатель, а {type(reader)}'
        assert reader.id == r.id, "id читателя не совпадает"
        assert reader.first_name == r.first_name, "first_name читателя не совпадает"
        assert reader.last_name == r.last_name, "last_name читателя не совпадает"
        assert reader.user_id == r.user_id, "user_id читателя не совпадает"

    def test_delete(self, reader_1, reader_dao):
        reader_dao.delete(reader_1)
        readers = reader_dao.get_all()

        assert len(readers) == 0, 'Книга не удалилась'

