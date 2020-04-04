from flask import jsonify, request

from myapp import app
from myapp.models import *


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return "hello", 200
