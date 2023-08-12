from copy import copy

from tools.security import compare_password


class TestUserViews:
    def test_get_by_user(self, client, user_1, headers_user):
        response = client.get('/users/', headers=headers_user)
        assert response.status_code == 200, f'Возвращается код {response.status_code} вместо 204'

        user = response.json
        user_keys = {'id', 'username'}

        assert user is not None, 'Возвращается None или пустой список'
        assert type(user) is dict, f'Возвращается {type(user)} вместо dict'
        assert user_keys == set(user.keys()), f'Ключи не совпадают'

    def test_put_by_user(self, client, user_1, headers_user):
        data = {
            'username': 'new_username'
        }
        response = client.put('/users/', json=data, headers=headers_user)

        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'
        assert user_1.username == data.get('username'), 'Имя пользователя не обновилось'

    def test_delete_by_user(self, client, user_1, headers_user, reader_1, user_service, reader_service):
        response = client.delete('/users/', headers=headers_user)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        users = user_service.get_all()
        assert len(users) == 0, 'Пользователь не удалился'

        readers = reader_service.get_all()
        assert len(readers) == 0, 'Читатель не удалился вместе с пользователем'

    def test_get_by_admin(self, client, admin, headers_admin, user_2):
        response = client.get(f'/users/{user_2.id}/', headers=headers_admin)
        assert response.status_code == 200, f'Возвращается код {response.status_code} вместо 204'

        user = response.json
        user_keys = {'id', 'username'}

        assert user is not None, 'Возвращается None или пустой список'
        assert type(user) is dict, f'Возвращается {type(user)} вместо dict'
        assert user_keys == set(user.keys()), f'Ключи не совпадают'
        assert user['id'] == user_2.id, 'id пользователей не совпадают'

    def test_put_by_admin(self, client, admin, headers_admin, user_2):
        data = {
            "username": "new_username"
        }
        response = client.put(f'/users/{user_2.id}/', json=data, headers=headers_admin)

        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'
        assert user_2.username == data.get('username'), 'Имя пользователя не обновилось'

    def test_delete_by_admin(self, client, admin, headers_admin, user_2, reader_1, reader_2, user_service,
                             reader_service):
        response = client.delete(f'/users/{user_2.id}/', headers=headers_admin)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        users = user_service.get_all()
        assert len(users) == 1, 'Пользователь не удалился'

        readers = reader_service.get_all()
        assert len(readers) == 1, 'Читатель не удалился вместе с пользователем'

    def test_get_all_by_admin(self, client, admin, headers_admin, user_2):
        response = client.get('/users/all/', headers=headers_admin)
        assert response.status_code == 200, f'Возвращается код {response.status_code} вместо 200'

        users = response.json
        user_keys = {'id', 'username'}

        assert users is not None, 'Возвращается None или пустой список'
        assert type(users) is list, f'Возвращается {type(users)} вместо list'
        assert type(users[0]) is dict, f'В списке находятся {type(users[0])} вместо dict'
        assert user_keys == set(users[0].keys()), f'Ключи не совпадают'

    def test_register(self, client, user_service, reader_service, hard_password_1):
        data = {
            "username": "new_username",
            "password": hard_password_1
        }
        response = client.post(f'/users/register/', json=data)
        assert response.status_code == 201, f'Возвращается код {response.status_code} вместо 201'

        user = user_service.get_all()[-1]
        assert user is not None, 'Возвращается None или пустой список'
        assert user.username == data.get('username'), 'Неверное имя пользователя'
        assert user.password != data.get('password'), 'Пароль в БД в нехешированном виде'
        assert compare_password(user.password, data.get('password')), 'Неверный пароль в БД'

        reader = reader_service.get_all()[-1]
        assert reader is not None, 'Возвращается None или пустой список'
        assert reader.user_id == user.id, 'id пользователя и читателя не совпадают'
        assert reader.id == user.id, 'id пользователя и читателя не совпадают'
        assert reader.first_name is None, 'Имя читателя не None при создании пользователя'
        assert reader.last_name is None, 'Фамилия читателя не None при создании пользователя'

    def test_change_password(self, client, user_1, headers_user, user_service, hard_password_1):
        old_password = copy(user_1.password)
        data = {
            'old_password': hard_password_1,
            'new_password': hard_password_1 + hard_password_1
        }
        response = client.post(f'/users/password/', json=data, headers=headers_user)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'
        assert old_password != user_1.password, 'Пароль не обновился'
        assert compare_password(user_1.password, data.get('new_password')), 'Новый пароль не установился'
