class TestReadersViews:
    def test_get_reader(self, client, headers_user, reader_1, reader_2):
        response = client.get('/readers/', headers=headers_user)
        assert response.status_code == 200, f'Возвращается код {response.status_code} вместо 200'

        reader: dict = response.json
        reader_keys = {'id', 'first_name', 'last_name', 'user_id', 'user'}

        assert reader is not None, 'Возвращается None или пустой список'
        assert type(reader) is dict, f'Возвращается {type(reader)} вместо dict'
        assert reader_keys == set(reader.keys()), f'Ключи не совпадают'

    def test_put(self, client, reader_1, headers_user, reader_service):
        data = {
            "first_name": "Имя_новое",
            "last_name": "Фамилия_новая"
        }
        response = client.put('/readers/', json=data, headers=headers_user)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        reader = reader_service.get_all()[-1]
        assert reader is not None, f'Вместо читателя вернулся None'
        assert reader.first_name == data.get('first_name'), 'Неверно установлено имя читателя'
        assert reader.last_name == data.get('last_name'), 'Неверно установлено фамилия читателя'

    def test_patch(self, client, reader_1, headers_user, reader_service):
        data = {
            "first_name": "Имя_новое",
            "last_name": "Фамилия_новая"
        }
        response = client.patch('/readers/', json=data, headers=headers_user)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        reader = reader_service.get_all()[-1]
        assert reader is not None, f'Вместо читателя вернулся None'
        assert reader.first_name == data.get('first_name'), 'Неверно установлено имя читателя'
        assert reader.last_name == data.get('last_name'), 'Неверно установлено фамилия читателя'

    def test_get_reader_by_admin(self, client, headers_admin, reader_2):
        response = client.get(f'/readers/{reader_2.id}', headers=headers_admin)
        assert response.status_code == 200, f'Возвращается код {response.status_code} вместо 200'

        reader = response.json
        reader_keys = {'id', 'first_name', 'last_name', 'user_id', 'user'}

        assert reader is not None, 'Возвращается None или пустой список'
        assert type(reader) is dict, f'Возвращается {type(reader)} вместо dict'
        assert reader_keys == set(reader.keys()), f'Ключи не совпадают'

    def test_put_by_admin(self, client, headers_admin, reader_2, reader_service):
        data = {
            "first_name": "Имя_новое",
            "last_name": "Фамилия_новая"
        }
        response = client.put(f'/readers/{reader_2.id}', json=data, headers=headers_admin)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        reader = reader_service.get_one(reader_2.id)
        assert reader is not None, f'Вместо читателя вернулся None'
        assert reader.first_name == data.get('first_name'), 'Неверно обновлено имя читателя'
        assert reader.last_name == data.get('last_name'), 'Неверно обновлено фамилия читателя'

    def test_patch_by_admin(self, client, headers_admin, reader_2,  reader_service):
        data = {
            "first_name": "Имя_новое",
            "last_name": "Фамилия_новая"
        }
        response = client.patch(f'/readers/{reader_2.id}', json=data, headers=headers_admin)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        reader = reader_service.get_one(reader_2.id)
        assert reader is not None, f'Вместо читателя вернулся None'
        assert reader.first_name == data.get('first_name'), 'Неверно обновлено имя читателя'
        assert reader.last_name == data.get('last_name'), 'Неверно обновлено фамилия читателя'

    def test_get_all_readers_by_admin(self, client, reader_1, reader_2, headers_admin):
        response = client.get('/readers/all', headers=headers_admin)
        assert response.status_code == 200, f'Возвращается код {response.status_code} вместо 200'

        readers: dict = response.json
        reader_keys = {'id', 'first_name', 'last_name', 'user_id', 'user'}

        assert readers is not None, 'Возвращается None или пустой список'
        assert type(readers) is list, f'Возвращается {type(readers)} вместо list'
        assert type(readers[0]) is dict, f'В списке находятся {type(readers[0])} вместо dict'
        assert reader_keys == set(readers[0].keys()), f'Ключи не совпадают'
