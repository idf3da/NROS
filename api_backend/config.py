import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_APP = 'app.py'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:JNHjneurokAJKajxznsuper!5791@147.78.64.237/neuro'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
