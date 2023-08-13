from flask import Flask

from api import api
from config import Config, config
from setup_db import db, migrate
from views import auth_ns, author_ns, book_ns, comment_ns, news_ns, reader_ns, user_ns


def create_app(app_config: Config):
    application = Flask(__name__)
    application.config.from_object(app_config)
    register_extensions(application)
    return application


def register_extensions(application: Flask):
    db.init_app(application)
    api.init_app(application)
    migrate.init_app(application, db)

    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(book_ns)
    api.add_namespace(reader_ns)
    api.add_namespace(author_ns)
    api.add_namespace(news_ns)
    api.add_namespace(comment_ns)

    @application.route('/ping')
    def ping_pong():
        return 'pong'


app_conf = config
app = create_app(app_conf)

if __name__ == '__main__':
    app.run()
