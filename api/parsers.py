from flask_restx.reqparse import RequestParser

# Book views
books_get: RequestParser = RequestParser()
books_get.add_argument(name='section', type=str, location='args', required=False)
books_get.add_argument(name='author_id', type=int, location='args', required=False)
books_get.add_argument(name='reader_id', type=int, location='args', required=False)

books_post: RequestParser = RequestParser()
books_post.add_argument(name='title', type=str, location='json', required=True)
books_post.add_argument(name='author_id', type=int, location='json', required=True)

books_put: RequestParser = RequestParser()
books_put.add_argument(name='title', type=str, location='json', required=True)
books_put.add_argument(name='author_id', type=int, location='json', required=True)

books_patch: RequestParser = RequestParser()
books_patch.add_argument(name='title', type=str, location='json', required=False)
books_patch.add_argument(name='author_id', type=int, location='json', required=False)

books_give: RequestParser = RequestParser()
books_give.add_argument(name='book_id', type=int, location='json', required=True)
books_give.add_argument(name='reader_id', type=int, location='json', required=True)

books_get_from_reader: RequestParser = RequestParser()
books_get_from_reader.add_argument(name='book_id', type=int, location='json', required=True)


# User views
user_post_register: RequestParser = RequestParser()
user_post_register.add_argument(name='username', type=str, location='json', required=True, )
user_post_register.add_argument(name='password', type=str, location='json', required=True)

user_post_password: RequestParser = RequestParser()
user_post_password.add_argument(name='old_password', type=str, location='json', required=True)
user_post_password.add_argument(name='new_password', type=str, location='json', required=True)

user_put: RequestParser = RequestParser()
user_put.add_argument(name='username', type=str, location='json', required=True)
