from app.dao.models.models_dao import User
from app.tools.security import get_hash


class TestUserDAO:
    def test_get_all(self, user_1, user_2, user_dao):
        users = user_dao.get_all()

        assert users is not None, "Возвращается None вместо пользователей"
        assert type(users) is list, 'Возвращается не список'
        assert len(users) == 2, f'Возвращается больше пользователей({len(users)}), чем ожидалось(2)'
        assert user_1 in users, "Первого пользователя нет в списке"
        assert user_2 in users, "Второго пользователя нет в списке"

    def test_get_one(self, user_1, user_dao):
        user = user_dao.get_one(user_1.id)

        assert user is not None, "Возвращается None вместо пользователя"
        assert type(user) is User, f'Возвращается не пользователь, а {type(user)}'
        assert user.id == user_1.id, "id пользователя не совпадает"
        assert user.username == user_1.username, "username пользователя не совпадает"
        assert user.password == user_1.password, "password пользователя не совпадает"
        assert user.role == user_1.role, "role пользователя не совпадает"

        user = user_dao.get_one(2)
        assert user is None, f'Возвращается {type(user)} вместо None'

    def test_get_by_name(self, user_1, user_dao):
        user = user_dao.get_by_name(user_1.username)

        assert user is not None, "Возвращается None вместо пользователя"
        assert type(user) is User, f'Возвращается не пользователь, а {type(user)}'
        assert user.id == user_1.id, "id пользователя не совпадает"
        assert user.username == user_1.username, "username пользователя не совпадает"
        assert user.password == user_1.password, "password пользователя не совпадает"
        assert user.role == user_1.role, "role пользователя не совпадает"

        user = user_dao.get_by_name('some_name')

        assert user is None, f'Возвращается {type(user)} вместо None'

    def test_save(self, user_dao):
        password = get_hash('1111')
        user_1 = User(
            username='name_1',
            password=password,
            role='user'
        )
        user_dao.save(user_1)
        user = user_dao.get_one(user_1.id)

        assert user is not None, "Возвращается None вместо пользователя"
        assert type(user) is User, f'Возвращается не пользователь, а {type(user)}'
        assert user.id == user_1.id, "id пользователя не совпадает"
        assert user.username == user_1.username, "username пользователя не совпадает"
        assert user.password == user_1.password, "password пользователя не совпадает"
        assert user.role == user_1.role, "role пользователя не совпадает"

    def test_delete(self, user_1, user_dao):
        user_dao.delete(user_1)
        users = user_dao.get_all()

        assert len(users) == 0, 'Пользователь не удален'
