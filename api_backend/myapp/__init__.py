from config import Config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db = SQLAlchemy(app)

from myapp.models import *

migrate = Migrate(app, db)
CORS(app)

from myapp import routes
from myapp import api_routes
