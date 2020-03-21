from flask import jsonify, request, abort
from flask_restful import Resource

from myapp import api
from myapp.models import *


def json_type(product_type):
    return {'id': product_type.id, 'name': product_type.name, 'price': product_type.price,
            'volume': product_type.volume}


def create_type(query):
    return ProductType(name=query['name'], price=query['price'], volume=query['volume'])


def create_type_with_id(query, product_type_id):
    return ProductType(id=product_type_id, name=query['name'], price=query['price'], volume=query['volume'])


def json_item(product_item):
    return {'id': product_item.id, 'product_type': json_type(product_item.product_type),
            'product_type_id': product_item.product_type_id,
            'count': product_item.count}


def create_item(query):
    return ProductItem(product_type_id=query['product_type_id'], count=query['count'])


def create_item_with_id(query, product_item_id):
    return ProductItem(id=product_item_id, product_type_id=query['product_type_id'], count=query['count'])


def json_group(product_group):
    return {'id': product_group.id,
            'product_items': [{'product_item': json_item(product_item)} for product_item in
                              product_group.product_items]}


def create_group(query):
    return ProductGroup(
        product_items=[ProductItem.query.get_or_404(product_item['product_item']['id']) for product_item in
                       query['product_items']])


def create_group_with_id(query, product_group_id):
    return ProductGroup(id=product_group_id,
                        product_items=[ProductItem.query.get_or_404(product_item['product_item']['id'])
                                       for product_item in query['product_items']])


def json_location(location):
    return {'id': location.id, 'address': location.address, 'latitude': location.latitude,
            'longitude': location.longitude}


def create_location(query):
    return Location(address=query['address'], latitude=query['latitude'],
                    longitude=query['longitude'])


def create_location_with_id(query, location_id):
    return Location(id=location_id, address=query['address'], latitude=query['latitude'],
                    longitude=query['longitude'])


class ProductTypeApi(Resource):
    def get(self, product_type_id):
        product_type = ProductType.query.get_or_404(product_type_id)
        return {'product_type': json_type(product_type)}, 200

    '''
    Example product type post query:
    {
        "count": 0,
        "name": "Salt",
        "price": 10,
        "volume": 1
    }
    
    '''

    def post(self):
        if not request.json:
            abort(400, "No data")
        product_type = create_type(request.json)
        db.session.add(product_type)
        db.session.commit()
        return {'product_type': json_type(product_type)}, 201

    def delete(self, product_type_id):
        product_type = ProductType.query.get_or_404(product_type_id)
        db.session.delete(product_type)
        db.session.commit()
        return "", 200

    def put(self, product_type_id):
        if not request.json:
            abort(400, "No data")
        db.session.delete(ProductType.query.get_or_404(product_type_id))
        db.session.commit()
        product_type = create_type_with_id(request.json, product_type_id)
        db.session.add(product_type)
        db.session.commit()
        return {'product_type': json_type(product_type)}, 201


class ProductItemApi(Resource):
    def get(self, product_item_id):
        product_item = ProductItem.query.get_or_404(product_item_id)
        return {'product_item': json_item(product_item)}, 200

    '''
    Example product item post query:
    {
        "product_type_id": 5,
        "count": 100000
    }
    '''

    def post(self):
        if not request.json:
            abort(400, "No data")
        product_item = create_item(request.json)
        db.session.add(product_item)
        db.session.commit()
        return {'product_item': json_item(product_item)}, 201

    def delete(self, product_item_id):
        product_item = ProductItem.query.get_or_404(product_item_id)
        db.session.delete(product_item)
        db.session.commit()
        return "", 200

    def put(self, product_item_id):
        if not request.json:
            abort(400, "No data")
        db.session.delete(ProductItem.query.get_or_404(product_item_id))
        db.session.commit()
        product_item = create_item_with_id(request.json, product_item_id)
        db.session.add(product_item)
        db.session.commit()
        return {'product_type': json_item(product_item)}, 201


class ProductGroupApi(Resource):
    def get(self, product_group_id):
        product_group = ProductGroup.query.get_or_404(product_group_id)
        return {'product_group': json_group(product_group)}, 200

    '''
    Example product group query:
    {
        "product_items": [
            {
                "product_item": {
                    "id": 3
                }
            },
            {
                "product_item": {
                    "id": 4
                }
            },
            {
                "product_item": {
                    "id": 5
                }
            }
        ]
    }
    '''

    def post(self):
        if not request.json:
            abort(400, "No data")
        product_group = create_group(request.json)
        db.session.add(product_group)
        db.session.commit()
        return {'product_group': json_group(product_group)}, 200

    def delete(self, product_group_id):
        product_group = ProductGroup.query.get_or_404(product_group_id)
        db.session.delete(product_group)
        db.session.commit()
        return "", 200

    def put(self, product_group_id):
        if not request.json:
            abort(400, "No data")
        delete_group = ProductGroup.query.get_or_404(product_group_id)
        db.session.delete(delete_group)
        db.session.commit()
        product_group = create_group_with_id(request.json, product_group_id)
        db.session.add(product_group)
        db.session.commit()
        return {'product_type': json_group(product_group)}, 201


class LocationApi(Resource):
    def get(self, location_id):
        location = Location.query.get_or_404(location_id)
        return {'location': json_location(location)}, 200

    '''
    Example location post query:
    {
        "address": "Yubileynaya, 13/2 - MSP Mytishchi",
        "longitude": 55.911905,
        "latitude": 37.719328
    }
    '''

    def post(self):
        if not request.json:
            abort(400, "No data")
        location = create_location(request.json)
        db.session.add(location)
        db.session.commit()
        return {'location': json_location(location)}, 200

    def delete_location(self, location_id):
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return "", 200

    def put(self, location_id):
        if not request.json:
            abort(400, "No data")
        db.session.delete(Location.query.get_or_404(location_id))
        db.session.commit()
        location = create_location_with_id(request.json, location_id)
        db.session.add(location)
        db.session.commit()
        return {'product_type': json_location(location)}, 201


api.add_resource(ProductTypeApi, '/api/product_type', '/api/product_type/<product_type_id>')
api.add_resource(ProductItemApi, '/api/product_item', '/api/product_item/<int:product_item_id>')
api.add_resource(ProductGroupApi, '/api/product_group', '/api/product_group/<product_group_id>')
api.add_resource(LocationApi, '/api/location', '/api/location/<location_id>')
