import os
from typing import Type
import dotenv

dotenv.load_dotenv()


class Config(object):
    SECRET_HERE = '249y823r9v8238r9u'
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PWD_HASH_SALT = os.getenv('PWD_HASH_SALT')
    PWD_HASH_ITERATIONS = os.getenv('PWD_HASH_ITERATIONS')
    JWT_SECRET = os.getenv('JWT_SECRET')
    JWT_ALGO = os.getenv('JWT_ALGO')
    HASH_NAME = os.getenv('HASH_NAME')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False


class ConfigFactory:
    flask_env = os.getenv('FLASK_ENV')

    @classmethod
    def get_config(cls) -> Type[Config]:
        if cls.flask_env == 'development':
            return DevelopmentConfig
        elif cls.flask_env == 'production':
            return ProductionConfig
        elif cls.flask_env == 'testing':
            return TestingConfig
        raise NotImplementedError


config = ConfigFactory.get_config()
