from flask import jsonify, request

from myapp import app
from myapp.models import *


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return "hello", 200


def get_type(product_type):
    return {'count': product_type.count, 'name': product_type.name, 'price': product_type.price,
            'volume': product_type.volume}


def create_type(query):
    return ProductType(count=query['count'], name=query['name'], price=query['price'], volume=query['volume'])


def get_item(product_item):
    return {'product_type': get_type(product_item.product_type), 'product_type_id': product_item.product_type_id,
            'count': product_item.count}


def create_item(query):
    return ProductItem(product_type_id=query['product_type_id'], count=query['count'])


@app.route('/api/product_type/<int:product_id>', methods=['GET'])
def get_product_type(product_id):
    product_type = ProductType.query.get_or_404(product_id)
    return jsonify({'product_type': get_type(product_type)}), 200


@app.route('/api/product_type', methods=['POST'])
def post_product_type():
    if not request.json:
        return 'Error 404', 404
    product_type = create_type(request.json)
    db.session.add(product_type)
    db.session.commit()
    return jsonify({'product_type': get_type(product_type)}), 200


@app.route('/api/product_item/<int:product_item_id>', methods=['GET'])
def get_product_item(product_item_id):
    product_item = ProductItem.query.get_or_404(product_item_id)
    return get_item(product_item), 200


@app.route('/api/product_item', methods=['POST'])
def post_product_item():
    if not request.json:
        return 'Error 404', 404
    product_item = create_item(request.json)
    db.session.add(product_item)
    db.session.commit()
    return jsonify({'product_item': get_item(product_item)}), 200
