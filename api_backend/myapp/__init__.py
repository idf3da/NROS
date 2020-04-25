from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS
from myapp.models import *
from myapp import routes
from myapp import api_routes

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
CORS(app)
