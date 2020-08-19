import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-secret-key'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:368368@localhost/app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
