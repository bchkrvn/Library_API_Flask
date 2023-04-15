from flask import Flask

from api.api import api
from config import Config, config
from setup_db import db, migrate
from views.auth_views import auth_ns
from views.authors_views import author_ns
from views.book_views import book_ns
from views.comment_views import comment_ns
from views.news_views import news_ns
from views.readers_views import reader_ns
from views.user_views import user_ns


def create_app(app_config: Config):
    application = Flask(__name__)
    application.config.from_object(app_config)
    register_extensions(application)
    return application


def register_extensions(appliacation_: Flask):
    db.init_app(appliacation_)
    api.init_app(appliacation_)
    migrate.init_app(appliacation_, db)

    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(book_ns)
    api.add_namespace(reader_ns)
    api.add_namespace(author_ns)
    api.add_namespace(news_ns)
    api.add_namespace(comment_ns)


app_conf = config
app = create_app(app_conf)

# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app.run()
