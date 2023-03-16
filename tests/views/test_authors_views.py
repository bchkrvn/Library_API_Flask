class TestAuthorViews:
    def test_get_authors(self, client, headers_user, author_1, author_2):
        response = client.get('/authors/', headers=headers_user)
        authors: dict = response.json
        author_keys = {'id', 'first_name', 'middle_name', 'last_name'}

        assert response.status_code == 200, f'Возвращается код {response.status_code} вместо 200'
        assert authors is not None, 'Возвращается None или пустой список'
        assert type(authors) is list, f'Возвращается {type(authors)} вместо list'
        assert type(authors[0]) is dict, f'В списке находятся {type(authors[0])} вместо dict'
        assert author_keys == set(authors[0].keys()), f'Ключи не совпадают'

    def test_post(self, client, headers_admin, author_service):
        data = {
            "first_name": "Имя_новое",
            "middle_name": "Отчество_новое",
            "last_name": "Фамилия_новая"
        }
        response = client.post('/authors/', json=data, headers=headers_admin)
        print(response.json)
        assert response.status_code == 201, f'Возвращается код {response.status_code} вместо 201'

        author = author_service.get_all()[-1]
        assert author is not None, f'Вместо автора вернулся None'
        assert author.first_name == data.get('first_name'), 'Неверно установлено имя автора'
        assert author.middle_name == data.get('middle_name'), 'Неверно установлено отчество автора'
        assert author.last_name == data.get('last_name'), 'Неверно установлено фамилия автора'

    def test_get_author(self, client, headers_user, author_1):
        response = client.get(f'/authors/{author_1.id}', headers=headers_user)
        author = response.json
        author_keys = ['id', 'first_name', 'middle_name', 'last_name', ]

        assert response.status_code == 200, f'Возвращается код {response.status_code} вместо 200'
        assert author is not None, 'Возвращается None или пустой словарь'
        assert type(author) is dict, f'Возвращается {type(author)} вместо dict'
        assert author_keys == list(author.keys()), f'Ключи не совпадают'

    def test_put(self, client, author_1, headers_admin, author_service):
        data = {
            "first_name": "Имя_новое",
            "middle_name": "Отчество_новое",
            "last_name": "Фамилия_новая"
        }
        response = client.put(f'/authors/1', json=data, headers=headers_admin)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        author = author_service.get_one(author_1.id)
        assert author is not None, f'Вместо автора вернулся None'
        assert author.first_name == data.get('first_name'), 'Неверно обновлено имя автора'
        assert author.middle_name == data.get('middle_name'), 'Неверно обновлено отчество автора'
        assert author.last_name == data.get('last_name'), 'Неверно обновлено фамилия автора'

    def test_patch(self, client, author_1, headers_admin, author_service):
        data = {
            "first_name": "Имя_новое",
            "middle_name": "Отчество_новое",
            "last_name": "Фамилия_новая"
        }
        response = client.patch(f'/authors/1', json=data, headers=headers_admin)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        author = author_service.get_one(author_1.id)
        assert author is not None, f'Вместо автора вернулся None'
        assert author.first_name == data.get('first_name'), 'Неверно обновлено имя автора'
        assert author.middle_name == data.get('middle_name'), 'Неверно обновлено отчество автора'
        assert author.last_name == data.get('last_name'), 'Неверно обновлено фамилия автора'

    def test_delete(self, client, author_1, author_2, headers_admin, author_service):
        response = client.delete(f'/authors/{author_2.id}', headers=headers_admin)
        assert response.status_code == 204, f'Возвращается код {response.status_code} вместо 204'

        authors = author_service.get_all()
        assert author_1 in authors, 'Удалился не тот автор'
        assert author_2 not in authors, 'Нужный автор не удалился'
