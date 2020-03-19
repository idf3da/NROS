import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_APP = 'app.py'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite_db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
