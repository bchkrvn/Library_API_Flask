from flask_restx.reqparse import RequestParser

books_get: RequestParser = RequestParser()
books_get.add_argument(name='section', type=str, location='args', required=False)
books_get.add_argument(name='author_id', type=int, location='args', required=False)
books_get.add_argument(name='reader_id', type=int, location='args', required=False)

books_post: RequestParser = RequestParser()
books_post.add_argument(name='title', type=str, location='json', required=False)
books_post.add_argument(name='author_id', type=int, location='json', required=False)

