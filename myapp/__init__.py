from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db = SQLAlchemy(app)
from myapp.models import *

migrate = Migrate(app, db)

from myapp import routes
from myapp import api_routes
