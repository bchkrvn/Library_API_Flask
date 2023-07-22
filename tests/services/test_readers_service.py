import pytest
from werkzeug.exceptions import NotFound

from application.dao.models.models_dao import Reader


class TestReaderService:
    def test_get_all(self, reader_1, reader_2, reader_service):
        readers = reader_service.get_all()

        assert readers is not None, "Возвращается None вместо читателей"
        assert type(readers) is list, 'Возвращается не список'
        assert len(readers) == 2, f'Возвращается больше читателей({len(readers)}), чем ожидалось(2)'
        assert reader_1 in readers, "Первого читателя нет в списке"
        assert reader_2 in readers, "Второго читателя нет в списке"

    def test_get_one(self, reader_1, reader_service):
        reader = reader_service.get_one(reader_1.id)

        assert reader is not None, "Возвращается None вместо читателя"
        assert type(reader) is Reader, f'Возвращается не читатель, а {type(reader)}'
        assert reader.id == reader_1.id, "id читателя не совпадает"
        assert reader.first_name == reader_1.first_name, "first_name читателя не совпадает"
        assert reader.last_name == reader_1.last_name, "last_name читателя не совпадает"
        assert reader.user_id == reader_1.user_id, "user_id читателя не совпадает"

        with pytest.raises(NotFound):
            reader_service.get_one(2)

    def test_create(self, user_1, reader_service):
        reader_service.create(user_1)
        reader = reader_service.get_all()[-1]

        assert reader is not None, "Возвращается None вместо читателя"
        assert type(reader) is Reader, f'Возвращается не читатель, а {type(reader)}'
        assert reader.id == user_1.id, "id читателя и пользователя не совпадают"
        assert reader.user == user_1, "пользователь и читатель не совпадают"

    def test_update(self, reader_1, reader_service):
        data = {
            'id': reader_1.id,
            'first_name': 'first_name_1',
            'last_name': 'last_name_1'
        }
        reader_service.update(data)
        reader = reader_service.get_one(reader_1.id)

        assert reader is not None, 'Возвращается None'
        assert reader.first_name == data.get('first_name'), 'first_name не обновился'
        assert reader.last_name == data.get('last_name'), 'last_name не обновился'

        # Неверный пользователь
        data = {
            'id': 2,
            'first_name': 'first_name_1',
            'last_name': 'last_name_1'
        }
        with pytest.raises(NotFound):
            reader_service.update(data)

    def test_update_partial(self, reader_1, reader_service):
        data = {
            'id': reader_1.id,
            'first_name': 'first_name_1',
            'last_name': 'last_name_1'
        }
        reader_service.update_partial(data)
        reader = reader_service.get_one(reader_1.id)

        assert reader is not None, 'Возвращается None'
        assert reader.first_name == data.get('first_name'), 'first_name не обновился'
        assert reader.last_name == data.get('last_name'), 'last_name не обновился'

        # Неверный пользователь
        data = {
            'id': 2,
            'first_name': 'first_name_1',
            'last_name': 'last_name_1'
        }
        with pytest.raises(NotFound):
            reader_service.update_partial(data)

    def test_delete(self, reader_1, reader_2, reader_service):
        reader_service.delete(reader_1.id)

        readers = reader_service.get_all()

        assert len(readers) == 1, 'Возвращается больше читателей, чем нужно'
        assert reader_2 in readers, 'Второй читатель удалился'

        # Неверный пользователь
        with pytest.raises(NotFound):
            reader_service.delete(3)
