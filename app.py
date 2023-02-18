from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db
from views.auth_views import auth_ns
from views.authors_views import author_ns
from views.book_views import book_ns
from views.readers_views import reader_ns
from views.user_views import user_ns


def create_app(app_config: Config):
    application = Flask(__name__)
    application.config.from_object(app_config)
    register_extensions(application)
    return application


def register_extensions(appliacation_: Flask):
    db.init_app(appliacation_)
    api = Api(appliacation_)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(book_ns)
    api.add_namespace(reader_ns)
    api.add_namespace(author_ns)


app_conf = Config()
app = create_app(app_conf)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
