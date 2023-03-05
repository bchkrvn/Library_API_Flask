import pytest
from werkzeug.exceptions import NotFound, BadRequest


class TestAuthService:
    def test_generate_token(self, user_1, auth_service):
        username = user_1.username
        password = '1111'

        tokens = auth_service.generate_token(username, password)

        assert tokens is not None, 'Токены не возвращаются'
        assert type(tokens) is dict, 'Возвращается не словарь'
        assert 'access_token' in tokens, 'В токенах нет access_token'
        assert 'refresh_token' in tokens, 'В токенах нет refresh_token'

        with pytest.raises(BadRequest):
            wrong_password = '2222'
            auth_service.generate_token(username, wrong_password)

        with pytest.raises(NotFound):
            auth_service.generate_token('wrong_name', password)

    def test_approve_refresh_token(self, user_1, auth_service):
        username = user_1.username
        password = '1111'
        tokens = auth_service.generate_token(username, password)

        refresh_token = tokens.get('refresh_token')
        new_tokens = auth_service.approve_refresh_token(refresh_token)

        assert new_tokens is not None, 'Токены не возвращаются'
        assert type(new_tokens) is dict, 'Возвращается не словарь'
        assert 'access_token' in new_tokens, 'В токенах нет access_token'
        assert 'refresh_token' in new_tokens, 'В токенах нет refresh_token'

        with pytest.raises(BadRequest):
            refresh_token = 'wrong_token'
            auth_service.approve_refresh_token(refresh_token)