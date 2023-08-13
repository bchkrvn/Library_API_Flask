import os
from typing import Type
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SECRET_HERE = os.getenv('SECRET_KEY')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PWD_HASH_SALT = bytes(os.getenv('PWD_HASH_SALT'), 'utf-8')
    PWD_HASH_ITERATIONS = int(os.getenv('PWD_HASH_ITERATIONS'))
    JWT_SECRET = bytes(os.getenv('JWT_SECRET'), 'utf-8')
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
