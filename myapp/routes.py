from flask import jsonify, request

from myapp import app
from myapp.models import *


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return "hello", 200


def json_type(product_type):
    return {'id': product_type.id, 'name': product_type.name, 'price': product_type.price,
            'volume': product_type.volume}


def create_type(query):
    return ProductType(name=query['name'], price=query['price'], volume=query['volume'])


def json_item(product_item):
    return {'id': product_item.id, 'product_type': json_type(product_item.product_type),
            'product_type_id': product_item.product_type_id,
            'count': product_item.count}


def create_item(query):
    return ProductItem(product_type_id=query['product_type_id'], count=query['count'])


def json_group(product_group):
    return {'id': product_group.id,
            'product_items': [{'product_item': json_item(product_item)} for product_item in
                              product_group.product_items]}


def create_group(query):
    return ProductGroup(
        product_items=[ProductItem.query.get_or_404(product_item['product_item']['id']) for product_item in
                       query['product_items']])


def json_location(location):
    return {'id': location.id, 'address': location.address, 'latitude': location.latitude,
            'longitude': location.longitude}


def create_location(query):
    return Location(address=query['address'], latitude=query['latitude'],
                    longitude=query['longitude'])


@app.route('/api/product_type/<int:product_id>', methods=['GET'])
def get_product_type(product_id):
    product_type = ProductType.query.get_or_404(product_id)
    return jsonify({'product_type': json_type(product_type)}), 200

'''
Example product type post query:
{
	"count" : 0,
	"name" : "Salt",
	"price" : 10,
	"volume" : 1
}
'''
@app.route('/api/product_type', methods=['POST'])
def post_product_type():
    if not request.json:
        return 'Error 404', 404
    product_type = create_type(request.json)
    db.session.add(product_type)
    db.session.commit()
    return jsonify({'product_type': json_type(product_type)}), 200


@app.route('/api/product_type/<int:product_id>', methods=['DELETE'])
def delete_product_type(product_id):
    product_type = ProductType.query.get_or_404(product_id)
    db.session.delete(product_type)
    db.session.commit()
    return "", 200


@app.route('/api/product_item/<int:product_item_id>', methods=['GET'])
def get_product_item(product_item_id):
    product_item = ProductItem.query.get_or_404(product_item_id)
    return jsonify({'product_item': json_item(product_item)}), 200

'''
Example product item post query:
{
	"product_type_id": 5,
	"count" : 100000
}
'''
@app.route('/api/product_item', methods=['POST'])
def post_product_item():
    if not request.json:
        return 'Error 404', 404
    product_item = create_item(request.json)
    db.session.add(product_item)
    db.session.commit()
    return jsonify({'product_item': json_item(product_item)}), 200


@app.route('/api/product_item/<int:product_item_id>', methods=['DELETE'])
def delete_product_item(product_item_id):
    product_item = ProductItem.query.get_or_404(product_item_id)
    db.session.delete(product_item)
    db.session.commit()
    return "", 200


@app.route('/api/product_group/<int:product_group_id>', methods=['GET'])
def get_product_group(product_group_id):
    product_group = ProductGroup.query.get_or_404(product_group_id)
    return jsonify({'product_group': json_group(product_group)}), 200


'''
Example product group query:
{
	"product_items" : [
		{
			"product_item": {
				"id" : 3
			}
		},
		{
		"product_item": {
				"id" : 4
			}
		},
		{
		"product_item": {
				"id" : 5
			}
		}
	]
}
'''
@app.route('/api/product_group', methods=['POST'])
def post_product_group():
    if not request.json:
        return 'Error 404', 404
    product_group = create_group(request.json)
    db.session.add(product_group)
    db.session.commit()
    return jsonify({'product_group': json_group(product_group)}), 200


@app.route('/api/product_group/<int:product_group_id>', methods=['DELETE'])
def delete_product_group(product_group_id):
    product_group = ProductGroup.query.get_or_404(product_group_id)
    db.session.delete(product_group)
    db.session.commit()
    return "", 200


@app.route('/api/location/<int:location_id>', methods=['GET'])
def get_location(location_id):
    location = Location.query.get_or_404(location_id)
    return jsonify({'location': json_location(location)}), 200

'''
Example location post query:
{
  "location": {
    "address": "Yubileynaya, 13/2 - MSP Mytishchi",
    "id": 4,
    "latitude": 37.719328,
    "longitude": 55.911905
  }
}
'''
@app.route('/api/location', methods=['POST'])
def post_location():
    if not request.json:
        return 'Error 404', 404
    location = create_location(request.json)
    db.session.add(location)
    db.session.commit()
    return jsonify({'location': json_location(location)}), 200


@app.route('/api/location/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    return "", 200
