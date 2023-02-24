from unittest.mock import MagicMock

import pytest as pytest

from dao.authors_dao import AuthorDAO
from dao.models.models_dao import Author


@pytest.fixture
def author_dao():
    a_1 = Author(id=1,
                 first_name='Имя_1',
                 middle_name='Отчество_1',
                 last_name='Фамилия_1')
    a_2 = Author(id=2,
                 first_name='Имя_2',
                 middle_name='Отчество_2',
                 last_name='Фамилия_2')
    author_dao = AuthorDAO(None)
    author_dao.get_one = MagicMock(return_value=a_1)
    author_dao.get_all = MagicMock(return_value=[a_1, a_2])

    return author_dao
