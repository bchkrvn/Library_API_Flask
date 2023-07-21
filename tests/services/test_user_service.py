import pytest
from werkzeug.exceptions import NotFound, BadRequest

from app.dao.models.models_dao import User, Reader
from app.tools import compare_password


class TestUserService:
    def test_get_all(self, user_1, user_2, user_service):
        users = user_service.get_all()

        assert users is not None, "Возвращается None вместо пользователей"
        assert type(users) is list, 'Возвращается не список'
        assert len(users) == 2, f'Возвращается больше пользователей({len(users)}), чем ожидалось(2)'
        assert user_1 in users, "Первого пользователя нет в списке"
        assert user_2 in users, "Второго пользователя нет в списке"

    def test_get_one(self, user_1, user_service):
        user = user_service.get_one(user_1.id)

        assert user is not None, "Возвращается None вместо пользователя"
        assert type(user) is User, f'Возвращается не пользователь, а {type(user)}'
        assert user.id == user_1.id, "id пользователя не совпадает"
        assert user.username == user_1.username, "username пользователя не совпадает"
        assert user.password == user_1.password, "password пользователя не совпадает"
        assert user.role == user_1.role, "role пользователя не совпадает"

        with pytest.raises(NotFound):
            user_service.get_one(2)

    def test_get_by_name(self, user_1, user_service):
        user = user_service.get_by_username(user_1.username)

        assert user is not None, "Возвращается None вместо пользователя"
        assert type(user) is User, f'Возвращается не пользователь, а {type(user)}'
        assert user.id == user_1.id, "id пользователя не совпадает"
        assert user.username == user_1.username, "username пользователя не совпадает"
        assert user.password == user_1.password, "password пользователя не совпадает"
        assert user.role == user_1.role, "role пользователя не совпадает"

        with pytest.raises(NotFound):
            user_service.get_by_username('some_name')

    def test_create(self, user_service, reader_service):
        data = {
            'username': 'name_1',
            'password': '1111'
        }
        user_service.create(data)
        user = user_service.get_all()[-1]
        reader = reader_service.get_all()[-1]

        assert user is not None, "Возвращается None вместо пользователя"
        assert type(user) is User, f'Возвращается не пользователь, а {type(user)}'
        assert user.id is not None, "id пользователя None"
        assert user.username == data.get('username'), "username пользователя не совпадает"
        assert user.password is not None, 'пароль пользователя не установлен'
        assert user.password != '1111', "Пароль не в хэш виде"
        assert user.role == 'user', "role пользователя не user"

        assert reader is not None, 'Читатель не создался вместо с пользователем'
        assert type(reader) is Reader, f'Возвращается не читатель, а {type(reader)}'
        assert reader.id == user.id, 'id читателя и пользователя не совпадают'

        # Повторяющийся username
        with pytest.raises(BadRequest):
            data_2 = {
                'username': 'name_1',
                'password': '1111'
            }
            user_service.create(data_2)

    def test_update(self, user_1, user_2, user_service):
        data = {
            'id': user_1.id,
            'username': 'new_username',
        }
        user_service.update(data)
        user = user_service.get_one(user_1.id)

        assert user.username == data.get('username'), 'username не обновился'

        # Несуществующий пользователь
        with pytest.raises(NotFound):
            data = {
                'id': 4,
                'username': 'new_username_2',
            }
            user_service.update(data)

        # username уже есть
        with pytest.raises(BadRequest):
            data = {
                'id': user_1.id,
                'username': user_2.username,
            }
            user_service.update(data)

    def test_delete(self, user_1, reader_1, user_service, reader_service):
        user_service.delete(user_1.id)
        users = user_service.get_all()
        readers = reader_service.get_all()

        assert len(users) == 0, 'Пользователь не удален'
        assert len(readers) == 0, 'Читатель не удалился'

        # Несуществующий пользователь
        with pytest.raises(NotFound):
            user_service.delete(1)

    def test_change_password(self, user_1, user_service, hard_password_1):
        data = {
            'user_id': user_1.id,
            'old_password': hard_password_1,
            'new_password': '2222',
        }
        user_service.change_password(data)
        user = user_service.get_one(user_1.id)

        assert not compare_password(user.password, hard_password_1), 'Пароль остался прежним'
        assert compare_password(user.password, '2222'), 'Пароль не обновился на новый'

        # Несуществующий пользователь
        with pytest.raises(NotFound):
            data = {
                'user_id': 2,
                'old_password': '1111',
                'new_password': '2222',
            }
            user_service.change_password(data)

        # Неверный пароль
        with pytest.raises(BadRequest):
            data = {
                'user_id': user_1.id,
                'old_password': 'wrong_password',
                'new_password': '2222',
            }
            user_service.change_password(data)
