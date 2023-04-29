import os
import dotenv
from typing import Type


class Config(object):
    DEBUG = True
    SECRET_HERE = '249y823r9v8238r9u'
    SQLALCHEMY_DATABASE_URI = "postgresql://lib_4:lib_4@pg/lib_4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PWD_HASH_SALT = b'secret here'
    PWD_HASH_ITERATIONS = 100_000
    JWT_SECRET = b'SeCR@t'
    JWT_ALGO = 'HS256'
    HASH_NAME = 'sha256'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False


class ConfigFactory:
    dotenv.load_dotenv(override=True)
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
