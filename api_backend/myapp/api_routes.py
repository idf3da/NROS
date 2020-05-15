"""Module that routes api requests"""
import datetime

import sqlalchemy as sa



import pickle

from flask import request, abort
from flask_restful import Resource
from myapp import api
from myapp.__init__ import db
from myapp.models import ProductType, ProductItem, ProductGroup, Location, \
    Warehouse, Shop, LSTM, Sale
import utils

import keras.backend.tensorflow_backend as tb #! костыль

def json_type(product_type):
    """Function converts product_type object into dictionary
    :param product_type: (ProductType) Product Type object
    :return dict: dictionary containing converted Product Type
    """
    return {'id': product_type.id, 'name': product_type.name,
            'price': product_type.price,
            'seasonality': product_type.seasonality}


def create_type(query):
    """ Function creates Product Type from query.
        :param query: (dict) Example: { name:"milk",
                                        price:1000,
                                        seasonality: 0
                                      }
        :return ProductType: Product Type object
    """
    return ProductType(name=query['name'], price=query['price'],
                       seasonality=query['seasonality'])


def create_type_with_id(query, product_type_id):
    """ Function creates Product Type with id from query.
            :param query: (dict) Example: { name:"milk",
                                            price:1000,
                                            seasonality: 0,
                                          }
            :param product_type_id: (int)
            :return ProductType: Product Type object
        """
    return ProductType(id=product_type_id, name=query['name'],
                       price=query['price'], seasonality=query['seasonality'])


def json_item(product_item):
    """ Function converts product_item object into dictionary
        :param product_item: (ProductItem) Product Item object
        :return dict: dictionary containing converted Product Item
    """
    return {'id': product_item.id,
            'product_type': json_type(product_item.product_type),
            'product_type_id': product_item.product_type_id,
            'count': product_item.count}


def create_item(query):
    """ Function creates Product Item from query.
        :param query: (dict) Example: {product_type_id: 1, count:10}
        :return ProductItem: Product Item object
    """
    return ProductItem(product_type_id=query['product_type_id'],
                       count=query['count'])


def create_item_with_id(query, product_item_id):
    """ Function creates Product Item with id from query.
            :param query: (dict) Example: {product_type_id: 1, count:10}
            :param product_item_id: (int)
            :return ProductItem: Product Item object
        """
    return ProductItem(id=product_item_id,
                       product_type_id=query['product_type_id'],
                       count=query['count'])


def json_group(product_group):
    """ Function converts product_group object into dictionary
        :param product_group: (ProductGroup) Product Group object
        :return dict: dictionary containing converted Product Group
    """
    return {'id': product_group.id,
            'product_items': [json_item(product_item) for product_item in
                              product_group.product_items]}


def create_group(query):
    """ Function creates Product Group from query.
        :param query: (dict) Example: {product_items: [1, 2, 3]}
        :return ProductGroup: Product Group object
    """
    return ProductGroup(
        product_items=[
            ProductItem.query.get_or_404(product_item['product_item']['id'])
            for product_item in
            query['product_items']])


def create_group_with_id(query, product_group_id):
    """ Function creates Product Group with id from query.
            :param query: (dict) Example: {product_items: [1, 2, 3]}
            :param product_group_id: (int)
            :return ProductGroup: Product Group object
        """
    product_items = [
        ProductItem.query.get_or_404(product_item['product_item']['id'])
        for product_item in query['product_items']
    ]
    return ProductGroup(id=product_group_id, product_items=product_items)


def json_location(location):
    """ Function converts Location object into dictionary
        :param location: (Location) Location object
        :return dict: dictionary containing converted Location
        """
    return {'id': location.id, 'address': location.address,
            'latitude': location.latitude, 'longitude': location.longitude}


def create_location(query):
    """ Function creates Location from query.
        :param query: (dict) Example: {address: "Yubileynaya Street, 13/2",
                                latitude: 55.911905,
                                longitude: 37.719328}
        :return Location: Location object
    """
    return Location(address=query['address'], latitude=query['latitude'],
                    longitude=query['longitude'])


def create_location_with_id(query, location_id):
    """ Function creates Location with id from query.
        :param query: (dict) Example: {
                                address: "Yubileynaya Street, 13/2",
                                latitude: 55.911905,
                                longitude: 37.719328}
        :param location_id: (int)
        :return Location: Location object
    """
    return Location(id=location_id, address=query['address'],
                    latitude=query['latitude'],
                    longitude=query['longitude'])


def json_warehouse(warehouse):
    """ Function converts Warehouse object into dictionary
        :param warehouse: (Warehouse) Warehouse object
        :return dict: dictionary containing converted Warehouse
        """
    return {'id': warehouse.id, 'location_id': warehouse.location_id,
            'fullness': warehouse.fullness, 'capacity': warehouse.capacity}


def create_warehouse(query):
    """ Function creates Warehouse from query.
        :param query: (dict) Example: { location_id: 1,
                                        fullness: 10,
                                        capacity: 20 }
        :return Warehouse: Warehouse object
    """
    return Warehouse(location_id=query['location_id'], fullness=query[
        'fullness'], capacity=query['capacity'])


def create_warehouse_with_id(query, warehouse_id):
    """ Function creates Warehouse with id from query.
        :param query: (dict) Example: { location_id: 1,
                                        fullness: 10,
                                        capacity: 20 }
        :param warehouse_id: (int)
        :return Warehouse: Warehouse object
    """
    return Warehouse(id=warehouse_id, location_id=query['location_id'],
                     fullness=query['fullness'], capacity=query['capacity'])


def json_shop(shop):
    """ Function converts Shop object into dictionary
        :param shop: (Shop) Shop object
        :return dict: dictionary containing converted Shop
        """
    return {'id': shop.id, 'location_id': shop.location_id,
            'fullness': shop.fullness, 'capacity': shop.capacity}


def create_shop(query):
    """ Function creates Shop from query.
        :param query: (dict) Example: { location_id: 1,
                                        fullness: 10,
                                        capacity: 20 }
        :return Shop: Shop object
    """
    return Shop(location_id=query['location_id'], fullness=query[
        'fullness'], capacity=query['capacity'])


def create_shop_with_id(query, shop_id):
    """ Function creates Shop with id from query.
        :param query: (dict) Example: { location_id: 1,
                                        fullness: 10,
                                        capacity: 20 }
        :param shop_id: (int)
        :return Shop: Shop object
    """
    return Shop(id=shop_id, location_id=query['location_id'],
                fullness=query['fullness'], capacity=query['capacity'])


def json_lstm(lstm):
    """ Function converts LSTM object into dictionary
        :param lstm: (LSTM) LSTM object
        :return dict: dictionary containing converted LSTM
        """
    return {'id': lstm.id, 'shop_id': lstm.shop_id,
            'product_type_id': lstm.product_type_id, 'alpha': lstm.alpha,
            'beta': lstm.beta, 'gamma': lstm.gamma}


def create_lstm(query):
    """ Function creates LSTM from query.
        :param query: (dict) Example: { shop_id: 1,
                                        product_type_id: 1,
                                        alpha: 0.1,
                                        beta: 0.1,
                                        gamma: 0.1
                                      }
        :return LSTM: LSTM object
    """
    before_range = None
    if 'before_range' in query:
        before_range = query['before_range'] + 1
    data = Sale.query.filter(Sale.shop_id == query['shop_id']).all()
    # print(data)
    tb._SYMBOLIC_SCOPE.value = True #! костыль
    models = LSTM.query.filter(LSTM.shop_id == query['shop_id'],LSTM.product_type_id==query['product_type_id']).all() #+user_id
    if models == []:
        slen = int(ProductType.query.filter(ProductType.id == query['product_type_id']).first().seasonality)
    else:
        slen = models[0].product_type.seasonality
    a,b,g,model,scaler,prediction = utils.trainModels(data,before_range,query['product_type_id'],models,slen)
    return LSTM(shop_id=query['shop_id'], product_type_id=query[
        'product_type_id'], alpha=a, beta=b,
                gamma=g,model = model,scope = scaler,prediction = prediction[0][0])


def create_lstm_with_id(query, lstm_id):
    """ Function creates LSTM with id from query.
        :param query: (dict) Example: { shop_id: 1,
                                        product_type_id: 1,
                                        alpha: 0.1,
                                        beta: 0.1,
                                        gamma: 0.1
                                      }
        :param lstm_id: (int)
        :return LSTM: LSTM object
    """
    before_range = None
    if 'before_range' in query:
        before_range = query['before_range'] + 1
    data = Sale.query.filter(Sale.shop_id == query['shop_id']).all()
    tb._SYMBOLIC_SCOPE.value = True #! костыль
    models = LSTM.query.filter(LSTM.shop_id == query['shop_id'],LSTM.product_type_id==query['product_type_id']).all() #+user_id
    if models == []:
        slen = int(ProductType.query.filter(ProductType.id == query['product_type_id']).first().seasonality)
    else:
        slen = models[0].product_type.seasonality
    a,b,g,model,scaler,prediction = utils.trainModels(data,before_range,query['product_type_id'],models,slen)
    return LSTM(id=lstm_id, shop_id=query['shop_id'], product_type_id=query[
        'product_type_id'],alpha=a, beta=b,
                gamma=g,model = model,scope = scaler,prediction = prediction[0][0])


def json_sale(sale):
    """ Function converts Sale object into dictionary
        :param sale: (Sale) Sale object
        :return dict: dictionary containing converted Sale
        """
    return {'id': sale.id, 'date': str(sale.date),
            'product_item_id': sale.product_item_id, 'shop_id': sale.shop_id}


def create_sale(query):
    """ Function creates Sale from query.
        :param query: (dict) Example: { date: '2011-11-04 00:05:23',
                                        product_item_id: 10,
                                        shop_id: 20 }
        :return Sale: Sale object
    """
    return Sale(date=datetime.datetime.fromisoformat(query['date']),
                product_item_id=query['product_item_id'],
                shop_id=query['shop_id'])


def create_sale_with_id(query, sale_id):
    """ Function creates Sale with id from query.
        :param query: (dict) Example: { date: '2011-11-04 00:05:23',
                                        product_item_id: 10,
                                        shop_id: 20 }
        :param sale_id: (int)
        :return Sale: Sale object
    """
    return Sale(id=sale_id, date=datetime.datetime.fromisoformat(query['date']),
                product_item_id=query['product_item_id'],
                shop_id=query['shop_id'])




def make_prediction(query):
    tb._SYMBOLIC_SCOPE.value = True #! костыль

    # warLen = 5
    # shopLen = 10
    # sklads = [{'sklad':j,'заполненость':1,'capacity':10000,'minimum':0,'shops':[[i,{'заполненость':1},{'capacity':10000},{'minimum':0}] for i in range(0,shopLen)]} for j in range(0,warLen)]

    # shops = Shop.query.all()
    # warhouse = Warehouse.query.all()
    sklads = []
    # for i in warhouse:
    #     sklads.append({i:[shops]})
    # print(sklads)
    stepG = query['step']
    models = LSTM.query.filter(LSTM.product_type_id==query['product_type_id']).all() #пока всё
    slen = ProductType.query.filter(ProductType.id == query['product_type_id']).first().seasonality
    full = []
    # print(ProductItem.query)
    for i in models:
        # print(pickle.loads(i.model).layers[0].input_shape)
        # model = pickle.loads(i.model)
        # test_shape = 2
        #pickle.loads(i.model).layers[0].input_shape[1]
        before_range = pickle.loads(i.model).layers[0].input_shape[-1] + 2 #i.before_range
        # print(model.layers[0].input_shape)

        sales = db.engine.execute('''
        SELECT sale.date::date, sum(product_item.count)
        FROM sale,product_item
        WHERE sale.shop_id = {0} AND product_item.product_type_id = {1}
        GROUP BY 1 ORDER BY 1 DESC LIMIT {2}
        '''.format(i.shop_id, query['product_type_id'], before_range)).fetchall()
        steps = db.engine.execute('''
        SELECT sale.date::date, sum(product_item.count)
        FROM sale,product_item
        WHERE sale.shop_id = {0} AND product_item.product_type_id = {1}
        GROUP BY 1 ORDER BY 1 DESC LIMIT {2}
        '''.format(i.shop_id, query['product_type_id'], stepG + before_range-1 if stepG >= before_range - 2 else before_range + 3)).fetchall()
        # print(step)
        year = db.engine.execute('''
        SELECT sale.date::date, sum(product_item.count)
        FROM sale,product_item
        WHERE sale.shop_id = {0} AND product_item.product_type_id = {1}
        GROUP BY 1 ORDER BY 1 DESC LIMIT {2}
        '''.format(i.shop_id, query['product_type_id'], 365)).fetchall()
        # print(sales)
        #war_id = Warhouse.query.filter(Warhouse.shop.id == models[i].shop_id).all()[0].id
        
        war_id = 1
        full.append({'sales' : sales, 'model':i, 'shop' : Shop.query.filter(Shop.id == i.shop_id).first(), 'war' : Warehouse.query.filter(Warehouse.id == war_id).first(),'before_range':before_range,'steps':steps,'slen':slen,'year':year})
        # print(full[-1])
    return utils.main_prediction(full)

class ListProductTypesApi(Resource):
    """ Class that gets all Product Types or creates new """

    @staticmethod
    def get():
        """ Method used to get list of all Product Types
            :return: list[ProductType]
        """
        product_types = ProductType.query.all()
        return {'product_types': [json_type(product_type) for product_type
                                  in
                                  product_types]}, 200

    @staticmethod
    def post():
        """ Create new Product Type
            Example product type post query:
            {
                "count": 0,
                "name": "Salt",
                "price": 10,
                "seasonality": 0
            }
            :return: jsonifyed ProductType
        """
        if not request.json:
            abort(400, "No data")
        product_type = create_type(request.json)
        db.session.add(product_type)
        db.session.commit()
        return {'product_type': json_type(product_type)}, 201


class ProductTypesApi(Resource):
    """ Class that gets/updates/deletes Product Type by id """

    @staticmethod
    def get(product_type_id):
        """ Get Product Type by id
            :param product_type_id: (int)
            :return ProductType: Product Type object
        """
        product_type = ProductType.query.get_or_404(product_type_id)
        return {'product_type': json_type(product_type)}, 200

    @staticmethod
    def delete(product_type_id):
        """ Deletes Product Type by id
            :param product_type_id: (int)
            :return: empty html
        """
        product_type = ProductType.query.get_or_404(product_type_id)
        db.session.delete(product_type)
        db.session.commit()
        return "", 200

    @staticmethod
    def put(product_type_id):
        """ Update/Create Product Type by id
            :param product_type_id: (int)
            :return: ProductType: Product Type object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(ProductType.query.get_or_404(product_type_id))
        db.session.commit()
        product_type = create_type_with_id(request.json, product_type_id)
        db.session.add(product_type)
        db.session.commit()
        return {'product_type': json_type(product_type)}, 201


class ListProductItemsApi(Resource):
    """ Class that gets all Product Items or creates new """

    @staticmethod
    def get():
        """ Method used to get list of all Product Items
        :return: list[ProductItem]
        """
        product_items = ProductItem.query.all()
        return {'product_items': [json_item(product_item) for product_item
                                  in
                                  product_items]}, 200

    @staticmethod
    def post():
        """ Create new Product Item
            Example product item post query:
            {
                "product_type_id": 5,
                "count": 100000
            }
            :return: jsonifyed ProductItem
        """
        if not request.json:
            abort(400, "No data")
        product_item = create_item(request.json)
        db.session.add(product_item)
        db.session.commit()
        return {'product_item': json_item(product_item)}, 201


class ProductItemsApi(Resource):
    """ Class that gets/updates/deletes Product Item by id """

    @staticmethod
    def get(product_item_id):
        """ Get Product Item by id
            :param product_item_id: (int)
            :return ProductItem: Product Item object
        """
        product_item = ProductItem.query.get_or_404(product_item_id)
        return {'product_item': json_item(product_item)}, 200

    @staticmethod
    def delete(product_item_id):
        """ Deletes Product Item by id
            :param product_item_id: (int)
            :return: empty html
        """
        product_item = ProductItem.query.get_or_404(product_item_id)
        db.session.delete(product_item)
        db.session.commit()
        return "", 200

    @staticmethod
    def put(product_item_id):
        """ Update/Create Product Item by id
            :param product_item_id: (int)
            :return: ProductItem: Product Item object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(ProductItem.query.get_or_404(product_item_id))
        db.session.commit()
        product_item = create_item_with_id(request.json, product_item_id)
        db.session.add(product_item)
        db.session.commit()
        return {'product_item': json_item(product_item)}, 201


class ListProductGroupsApi(Resource):
    """ Class that gets all Product Groups or creates new """

    @staticmethod
    def get():
        """ Method used to get list of all Product Groups
                :return: list[ProductGroup]
                """
        product_groups = ProductGroup.query.all()
        return {'product_groups': [json_group(product_group) for
                                   product_group
                                   in
                                   product_groups]}, 200

    @staticmethod
    def post():
        """ Create new Product Group
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
            :return: jsonifyed ProductGroup
            """
        if not request.json:
            abort(400, "No data")
        product_group = create_group(request.json)
        db.session.add(product_group)
        db.session.commit()
        return {'product_group': json_group(product_group)}, 200


class ProductGroupsApi(Resource):
    """ Class that gets/updates/deletes Product Group by id """

    @staticmethod
    def get(product_group_id):
        """ Get Product Group by id
            :param product_group_id:
            :return ProductGroup: Product Group object
        """
        product_group = ProductGroup.query.get_or_404(product_group_id)
        return {'product_group': json_group(product_group)}, 200

    @staticmethod
    def delete(product_group_id):
        """ Deletes Product Group by id
            :param product_group_id: (int)
            :return: empty html
        """
        product_group = ProductGroup.query.get_or_404(product_group_id)
        db.session.delete(product_group)
        db.session.commit()
        return "", 200

    @staticmethod
    def put(product_group_id):
        """ Update/Create Product Group by id
            :param product_group_id: (int)
            :return: ProductGroup: Product Group object
        """
        if not request.json:
            abort(400, "No data")
        delete_group = ProductGroup.query.get_or_404(product_group_id)
        db.session.delete(delete_group)
        db.session.commit()
        product_group = create_group_with_id(request.json,
                                             product_group_id)
        db.session.add(product_group)
        db.session.commit()
        return {'product_group': json_group(product_group)}, 201


class ListLocationsApi(Resource):
    """ Class that gets all Locations or creates new """

    @staticmethod
    def get():
        """ Method used to get list of all Locations
            :return: list[Location]
        """
        locations = Location.query.all()
        return {'locations': [json_location(location) for location in
                              locations]}, 200

    @staticmethod
    def post():
        """ Create new Location
            Example location post query:
            {
                "address": "Lva Tolstogo Street, 16 - MSP Yandex",
                "latitude": 55.733969,
                "longitude": 37.587093
            }
            :return: jsonifyed Location
        """
        if not request.json:
            abort(400, "No data")
        location = create_location(request.json)
        db.session.add(location)
        db.session.commit()
        return {'location': json_location(location)}, 200


class LocationApi(Resource):
    """ Class that gets/updates/deletes Location by id """

    @staticmethod
    def get(location_id):
        """ Get Location by id
            :param location_id: (int)
            :return Location: Location object
        """
        location = Location.query.get_or_404(location_id)
        return {'location': json_location(location)}, 200

    @staticmethod
    def delete(location_id):
        """ Deletes Location by id
            :param location_id: (int)
            :return: empty html
        """
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()
        return "", 200

    @staticmethod
    def put(location_id):
        """ Update/Create Location by id
            :param location_id: (int)
            :return: Location: Location object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(Location.query.get_or_404(location_id))
        db.session.commit()
        location = create_location_with_id(request.json, location_id)
        db.session.add(location)
        db.session.commit()
        return {'location': json_location(location)}, 201


class ListWarehousesApi(Resource):
    """ Class that gets all Warehouses or creates new """

    @staticmethod
    def get():
        """ Method used to get list of all Warehouses
            :return: list[Warehouse]
        """
        warehouses = Warehouse.query.all()
        return {'warehouses': [json_warehouse(warehouse) for warehouse in
                               warehouses]}, 200

    @staticmethod
    def post():
        """ Create new Warehouse
            Example warehouse post query:
            {
                "warehouse_id": 1,
                "fullness": 10,
                "capacity": 20
            }
            :return: jsonifyed Warehouse
        """
        if not request.json:
            abort(400, "No data")
        warehouse = create_warehouse(request.json)
        db.session.add(warehouse)
        db.session.commit()
        return {'warehouse': json_warehouse(warehouse)}, 200


class WarehouseApi(Resource):
    """ Class that gets/updates/deletes Warehouse by id """

    @staticmethod
    def get(warehouse_id):
        """ Get Warehouse by id
            :param warehouse_id: (int)
            :return Warehouse: Warehouse object
        """
        warehouse = Warehouse.query.get_or_404(warehouse_id)
        return {'warehouse': json_warehouse(warehouse)}, 200

    @staticmethod
    def delete(warehouse_id):
        """ Deletes Warehouse by id
            :param warehouse_id: (int)
            :return: empty html
        """
        warehouse = Warehouse.query.get_or_404(warehouse_id)
        db.session.delete(warehouse)
        db.session.commit()
        return "", 200

    @staticmethod
    def put(warehouse_id):
        """ Update/Create Warehouse by id
            :param warehouse_id: (int)
            :return: Warehouse: Warehouse object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(Warehouse.query.get_or_404(warehouse_id))
        db.session.commit()
        warehouse = create_warehouse_with_id(request.json, warehouse_id)
        db.session.add(warehouse)
        db.session.commit()
        return {'warehouse': json_warehouse(warehouse)}, 201


class ListShopsApi(Resource):
    """ Class that gets all Shops or creates new """

    @staticmethod
    def get():
        """ Method used to get list of all Shops
            :return: list[Shop]
        """
        shops = Shop.query.all()
        return {'shops': [json_shop(shops) for shops in shops]}, 200

    @staticmethod
    def post():
        """ Create new Shop
            Example shop post query:
            {
                "shop_id": 1,
                "fullness": 10,
                "capacity": 20
            }
            :return: jsonifyed Shop
        """
        if not request.json:
            abort(400, "No data")
        shop = create_shop(request.json)
        db.session.add(shop)
        db.session.commit()
        return {'shop': json_shop(shop)}, 200


class ShopApi(Resource):
    """ Class that gets/updates/deletes Shop by id """

    @staticmethod
    def get(shop_id):
        """ Get Shop by id
            :param shop_id: (int)
            :return Shop: Shop object
        """
        shop = Shop.query.get_or_404(shop_id)
        return {'shop': json_shop(shop)}, 200

    @staticmethod
    def delete(shop_id):
        """ Deletes Shop by id
            :param shop_id: (int)
            :return: empty html
        """
        shop = Shop.query.get_or_404(shop_id)
        db.session.delete(shop)
        db.session.commit()
        return "", 200

    @staticmethod
    def put(shop_id):
        """ Update/Create Shop by id
            :param shop_id: (int)
            :return: Shop: Shop object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(Shop.query.get_or_404(shop_id))
        db.session.commit()
        shop = create_shop_with_id(request.json, shop_id)
        db.session.add(shop)
        db.session.commit()
        return {'shop': json_shop(shop)}, 201


class ListLSTMsApi(Resource):
    """ Class that gets all LSTMs or creates new """

    @staticmethod
    def get():
        """ Method used to get list of all LSTMs
            :return: list[LSTM]
        """
        lstms = LSTM.query.all()
        return {'LSTMs': [json_lstm(lstm) for lstm in lstms]}, 200

    @staticmethod
    def post():
        """ Create new LSTM
            Example LSTM post query:
            {
                "shop_id": 1,
                "product_type_id": 1
                "alpha": 0.1,
                "beta": 0.1,
                "gamma": 0.1
            }
            :return: jsonifyed LSTM
        """
        if not request.json:
            abort(400, "No data")
        lstm = create_lstm(request.json)
        db.session.add(lstm)
        db.session.commit()
        return {'lstm': json_lstm(lstm)}, 200


class LSTMApi(Resource):
    """ Class that gets/updates/deletes LSTM by id """

    @staticmethod
    def get(lstm_id):
        """ Get LSTM by id
            :param lstm_id: (int)
            :return LSTM: LSTM object
        """
        lstm = LSTM.query.get_or_404(lstm_id)
        return {'lstm': json_lstm(lstm)}, 200

    @staticmethod
    def delete(lstm_id):
        """ Deletes LSTM by id
            :param lstm_id: (int)
            :return: empty html
        """
        lstm = LSTM.query.get_or_404(lstm_id)
        db.session.delete(lstm)
        db.session.commit()
        return "", 200

    @staticmethod
    def put(lstm_id):
        """ Update/Create LSTM by id
            :param lstm_id: (int)
            :return: LSTM: LSTM object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(LSTM.query.get_or_404(lstm_id))
        db.session.commit()
        lstm = create_lstm_with_id(request.json, lstm_id)
        db.session.add(lstm)
        db.session.commit()
        return {'lstm': json_lstm(lstm)}, 201


class ListSalesApi(Resource):
    """ Class that gets all Sales or creates new """

    @staticmethod
    def get():
        """ Method used to get list of all Sales
            :return: list[Sale]
        """
        sales = Sale.query.all()
        return {'sales': [json_sale(sales) for sales in sales]}, 200

    @staticmethod
    def post():
        """ Create new Sale
            Example sale post query:
            {
                "date": '2011-11-04 00:05:23',
                "product_item_id": 10,
                "shop_id": 20
            }
            :return: jsonifyed Sale
        """
        if not request.json:
            abort(400, "No data")
        sale = create_sale(request.json)
        db.session.add(sale)
        db.session.commit()
        print(sale)
        return {'sale': json_sale(sale)}, 200


class SaleApi(Resource):
    """ Class that gets/updates/deletes Sale by id """

    @staticmethod
    def get(sale_id):
        """ Get Sale by id
            :param sale_id: (int)
            :return Sale: Sale object
        """
        sale = Sale.query.get_or_404(sale_id)
        return {'sale': json_sale(sale)}, 200

    @staticmethod
    def delete(sale_id):
        """ Deletes Sale by id
            :param sale_id: (int)
            :return: empty html
        """
        sale = Sale.query.get_or_404(sale_id)
        db.session.delete(sale)
        db.session.commit()
        return "", 200

    @staticmethod
    def put(sale_id):
        """ Update/Create Sale by id
            :param sale_id: (int)
            :return: Sale: Sale object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(Sale.query.get_or_404(sale_id))
        db.session.commit()
        sale = create_sale_with_id(request.json, sale_id)
        db.session.add(sale)
        db.session.commit()
        return {'sale': json_sale(sale)}, 201

class PredictApi(Resource):
    """ Class that make predictions """

    @staticmethod
    def get():
        """ Method used to get list of all Sales
            :return: list[Sale]
        """
        sales = Sale.query.all()
        return {'sales': [json_sale(sales) for sales in sales]}, 200

    @staticmethod
    def post():
        """ Create new Sale
            Example sale post query:
            {
                "date": '2011-11-04 00:05:23',
                "product_item_id": 10,
                "shop_id": 20
            }
            :return: jsonifyed Sale
        """
        if not request.json:
            abort(400, "No data")
        sale = make_prediction(request.json)
        db.session.add(sale)
        db.session.commit()
        print(sale)
        return {'sale': json_sale(sale)}, 200

api.add_resource(ProductTypesApi, '/api/product_types/<product_type_id>')
api.add_resource(ProductItemsApi,
                 '/api/product_items/<int:product_item_id>')
api.add_resource(ProductGroupsApi,
                 '/api/product_groups/<product_group_id>')
api.add_resource(LocationApi, '/api/locations/<location_id>')
api.add_resource(WarehouseApi, '/api/warehouses/<warehouse_id>')
api.add_resource(ShopApi, '/api/shops/<shop_id>')
api.add_resource(LSTMApi, '/api/lstms/<lstm_id>')
api.add_resource(SaleApi, '/api/sales/<sale_id>')
api.add_resource(ListProductTypesApi, '/api/product_types')
api.add_resource(ListProductItemsApi, '/api/product_items')
api.add_resource(ListProductGroupsApi, '/api/product_groups')
api.add_resource(ListLocationsApi, '/api/locations')
api.add_resource(ListWarehousesApi, '/api/warehouses')
api.add_resource(ListShopsApi, '/api/shops')
api.add_resource(ListLSTMsApi, '/api/lstms')
api.add_resource(ListSalesApi, '/api/sales')

#danger(cum) zone
api.add_resource(PredictApi, '/api/predict')


    # data = Sale.query.filter(Sale.shop_id==query['shop_id'], Sale.product_item.product_type_id==query['product_type_id']).all()
        # data = Sale.query.join(ProductItem).filter(Sale.shop_id==query['shop_id'],ProductItem.product_type_id == query['product_type_id']).all()
        # data = ProductItem.query.join(Sale).filter(Sale.shop_id==query['shop_id'],ProductItem.product_type_id == query['product_type_id']).all()
        # data = db.session.query(Sale,ProductItem).filter(Sale.shop_id==query['shop_id'],ProductItem.product_type_id == query['product_type_id']).all()