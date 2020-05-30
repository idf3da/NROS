"""Module that routes api requests"""
import datetime

import sqlalchemy as sa



import pickle

from flask import request, abort
from flask_restful import Resource
from myapp import api
from myapp.__init__ import db
from myapp.models import ProductType,Point, LSTM, Sale
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








def json_point(point):
    """ Function converts Point object into dictionary
        :param point: (Point) Point object
        :return dict: dictionary containing converted Point
        """
    return {'id': point.id,
            'fullness': point.fullness,
            'address':point.address,'latitude':point.latitude,'longitude':point.longitude,
            'capacity':point.capacity,'minimum':point.minimum,'shop':point.shop, 'shop_id':point.shop_id}


def create_point(query):
    """ Function creates Point from query.
        :param query: (dict) Example: { location_id: 1,
                                        fullness: 10,
                                        capacity: 20 }
        :return Point: Point object
    """
    return Point(address=query['address'], fullness=query['fullness'], capacity=query['capacity'],
     latitude=query['latitude'],longitude=query['longitude'], minimum=query['minimum'], shop=query['shop'], shop_id = query['shop_id'])        


def create_point_with_id(query, point_id):
    """ Function creates Shop with id from query.
        :param query: (dict) Example: { location_id: 1,
                                        fullness: 10,
                                        capacity: 20 }
        :param shop_id: (int)
        :return Shop: Shop object
    """
    return Point(id = point_id,address=query['address'], fullness=query['fullness'], capacity=query['capacity'],
     latitude=query['latitude'],longitude=query['longitude'], minimum=query['minimum'], shop=query['shop'])       


def json_lstm(lstm):
    """ Function converts LSTM object into dictionary
        :param lstm: (LSTM) LSTM object
        :return dict: dictionary containing converted LSTM
        """
    return {'id': lstm.id, 'point_id': lstm.point_id,
            'product_type_id': lstm.product_type_id, 'alpha': lstm.alpha,
            'beta': lstm.beta, 'gamma': lstm.gamma, 'prediction':lstm.prediction,
            'before_range':lstm.before_range,'lstm_pred':lstm.lstm_pred,
            'listForvector':lstm.listForvector,'realSpros':lstm.realSpros}


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
        before_range = query['before_range']
    data = db.engine.execute('''
    with dates as (
        select generate_series(
            (select min(date) from sale), (select max(date) from sale), '1 day'::interval
        ) as date
    )
    select
        dates.date,
        coalesce(sum(sale.count), 0)
        from dates
        left join sale
            on date_part('day', sale.date) = date_part('day', dates.date)
            and date_part('month', sale.date) = date_part('month', dates.date)
            and date_part('year', sale.date) = date_part('year', dates.date)
            and sale.point_id = {0}
            and sale.product_type_id = {1}
        group by 1 order by 1 desc
    '''.format(query['point_id'], query['product_type_id'])).fetchall() #and product_item.product_type_id = {1} and sale.product_item_id = product_item.id
    tb._SYMBOLIC_SCOPE.value = True #! костыль
    model = LSTM.query.filter(LSTM.point_id == query['point_id'],LSTM.product_type_id==query['product_type_id']).first() #+user_id
    if model == None:
        slen = int(ProductType.query.filter(ProductType.id == query['product_type_id']).first().seasonality)
    else:
        slen = model.product_type.seasonality
        before_range = model.before_range
    a,b,g,model,scaler,prediction,before_range,lstm_prediciton = utils.trainModelsAndPredict(data,before_range + 1,model,slen)
    stepG = 2

    if a == -1:
        steps = db.engine.execute('''
        with dates as (
            select generate_series(
                (select min(date) from sale), (select max(date) from sale), '1 day'::interval
            ) as date
        )
        select
            dates.date,
            coalesce(sum(sale.count), 0)
            from dates
            left join sale
                on date_part('day', sale.date) = date_part('day', dates.date)
                and date_part('month', sale.date) = date_part('month', dates.date)
                and date_part('year', sale.date) = date_part('year', dates.date)
                and sale.point_id = {0}
                and sale.product_type_id = {1}
            group by 1 order by 1 desc limit {2}
        '''.format(query['point_id'], query['product_type_id'], stepG+3 if stepG >= before_range else before_range+3)).fetchall()
        contRes = utils.predict_step(steps,before_range = before_range+1,scaler = scaler,model = model)
        spros,listForvector,realSpros = lstm_prediciton,contRes[0],contRes[1]
    else:
        steps = db.engine.execute('''
        with dates as (
            select generate_series(
                (select min(date) from sale), (select max(date) from sale), '1 day'::interval
            ) as date
        )
        select
            dates.date,
            coalesce(sum(sale.count), 0)
            from dates
            left join sale
                on date_part('day', sale.date) = date_part('day', dates.date)
                and date_part('month', sale.date) = date_part('month', dates.date)
                and date_part('year', sale.date) = date_part('year', dates.date)
                and sale.point_id = {0}
                and sale.product_type_id = {1}
            group by 1 order by 1 desc limit {2}
        '''.format(query['point_id'], query['product_type_id'], 367)).fetchall()
        resR = utils.predictWinters([row[1] for row in steps],a,b,g,slen,stepG)
        spros,listForvector,realSpros = prediction,resR[0],resR[1]

    print(spros,listForvector,realSpros)


    return LSTM(point_id=query['point_id'], product_type_id=query[
        'product_type_id'], alpha=a, beta=b,
                gamma=g,model = pickle.dumps(model),scope = pickle.dumps(scaler),prediction = prediction,
                lstm_pred = lstm_prediciton,before_range = before_range,
                listForvector = listForvector,realSpros = realSpros) #before_range = before_range


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

    data = db.engine.execute('''
    with dates as (
        select generate_series(
            (select min(date) from sale), (select max(date) from sale), '1 day'::interval
        ) as date
    )
    select
        dates.date,
        coalesce(sum(sale.count), 0)
        from dates
        left join sale
            on date_part('day', sale.date) = date_part('day', dates.date)
            and date_part('month', sale.date) = date_part('month', dates.date)
            and date_part('year', sale.date) = date_part('year', dates.date)
            and sale.point_id = {0}
            and sale.product_type_id = {1}
        group by 1 order by 1 desc
    '''.format(query['point_id'], query['product_type_id'])).fetchall()
    # print(data,'data')
    # data = Sale.query.filter(Sale.shop_id == query['shop_id']).all()
    tb._SYMBOLIC_SCOPE.value = True #! костыль
    models = LSTM.query.filter(LSTM.point_id == query['point_id'],LSTM.product_type_id==query['product_type_id']).all() #+user_id
    if models == []:
        slen = int(ProductType.query.filter(ProductType.id == query['product_type_id']).first().seasonality)
    else:
        slen = models[0].product_type.seasonality
    a,b,g,model,scaler,prediction,before_range,lstm_prediciton = utils.trainModels(data,before_range,models,slen)

    stepG = 2

    if a == -1:
        steps = db.engine.execute('''
        with dates as (
            select generate_series(
                (select min(date) from sale), (select max(date) from sale), '1 day'::interval
            ) as date
        )
        select
            dates.date,
            coalesce(sum(sale.count), 0)
            from dates
            left join sale
                on date_part('day', sale.date) = date_part('day', dates.date)
                and date_part('month', sale.date) = date_part('month', dates.date)
                and date_part('year', sale.date) = date_part('year', dates.date)
                and sale.point_id = {0}
                and sale.product_type_id = {1}
            group by 1 order by 1 desc limit {2}
        '''.format(query['point_id'], query['product_type_id'], stepG + before_range-1 if stepG >= before_range - 2 else before_range + 3)).fetchall()
        contRes = utils.predict_sales([],step = steps,before_range = before_range,scaler = scaler,model = model)
        spros,listForvector,realSpros = lstm_prediciton,contRes[0],contRes[1]
    else:
        steps = db.engine.execute('''
        with dates as (
            select generate_series(
                (select min(date) from sale), (select max(date) from sale), '1 day'::interval
            ) as date
        )
        select
            dates.date,
            coalesce(sum(sale.count), 0)
            from dates
            left join sale
                on date_part('day', sale.date) = date_part('day', dates.date)
                and date_part('month', sale.date) = date_part('month', dates.date)
                and date_part('year', sale.date) = date_part('year', dates.date)
                and sale.point_id = {0}
                and sale.product_type_id = {1}
            group by 1 order by 1 desc limit {2}
        '''.format(query['point_id'], query['product_type_id'], 367)).fetchall()
        resR = utils.predict_rare([],a,b,g,slen,[row[1] for row in steps],stepG)
        spros,listForvector,realSpros = prediction,resR[0],resR[1]

    print(spros,listForvector,realSpros)






    return LSTM(id = lstm_id,point_id=query['point_id'], product_type_id=query[
        'product_type_id'], alpha=a, beta=b,
                gamma=g,model = model,scope = scaler,prediction = prediction,
                lstm_pred = lstm_prediciton,before_range = before_range,
                listForvector = listForvector,realSpros = realSpros)


def json_sale(sale):
    """ Function converts Sale object into dictionary
        :param sale: (Sale) Sale object
        :return dict: dictionary containing converted Sale
        """
    return {'id': sale.id, 'date': str(sale.date),
            'count': sale.count, 'point_id': sale.point_id, 'product_type_id':sale.product_type_id}


def create_sale(query):
    """ Function creates Sale from query.
        :param query: (dict) Example: { date: '2011-11-04 00:05:23',
                                        product_item_id: 10,
                                        shop_id: 20 }
        :return Sale: Sale object
    """
    return Sale(date=datetime.datetime.fromisoformat(query['date']),
                product_type_id=query['product_type_id'],
                point_id=query['point_id'],
                count = query['count'])


def create_sale_with_id(query, sale_id):
    """ Function creates Sale with id from query.
        :param query: (dict) Example: { date: '2011-11-04 00:05:23',
                                        product_item_id: 10,
                                        shop_id: 20 }
        :param sale_id: (int)
        :return Sale: Sale object
    """
    return Sale(id=sale_id, date=datetime.datetime.fromisoformat(query['date']),
                product_type_id=query['product_type_id'],
                point_id=query['point_id'],
                count = query['count'])




def make_prediction(query):
    tb._SYMBOLIC_SCOPE.value = True #! костыль
    models = LSTM.query.filter(LSTM.product_type_id==query['product_type_id']).all() #пока всё
    slen = ProductType.query.filter(ProductType.id == query['product_type_id']).first().seasonality
    full = []
    for i in models:
        full.append({'spros':i.lstm_pred if i.alpha == -1 else i.prediction, 'shop' : Point.query.filter(Point.id == i.point_id,Point.shop == True).first(), 'war' : Point.query.filter(i.point_id.in_(Point.shop_id),Point.shop == False).first(),
       'listForvector':i.listForvector,'realSpros':i.realSpros,'price':i.product_type.price})
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

class ListPointsApi(Resource):
    """ Class that gets all Shops or creates new """

    @staticmethod
    def get():
        """ Method used to get list of all Shops
            :return: list[Shop]
        """
        points = Point.query.all()
        return {'points': [json_point(points) for points in points]}, 200

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
        point = create_point(request.json)
        db.session.add(point)
        db.session.commit()
        return {'point': json_point(point)}, 200


class PointApi(Resource):
    """ Class that gets/updates/deletes Point by id """

    @staticmethod
    def get(point_id):
        """ Get Shop by id
            :param shop_id: (int)
            :return Shop: Shop object
        """
        point = Point.query.get_or_404(point_id)
        return {'shop': json_point(point)}, 200

    @staticmethod
    def delete(point_id):
        """ Deletes Shop by id
            :param shop_id: (int)
            :return: empty html
        """
        point = Point.query.get_or_404(point_id)
        db.session.delete(point)
        db.session.commit()
        return "", 200

    @staticmethod
    def put(point_id):
        """ Update/Create Shop by id
            :param shop_id: (int)
            :return: Shop: Shop object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(Point.query.get_or_404(point_id))
        db.session.commit()
        point = create_point_with_id(request.json, point_id)
        db.session.add(point)
        db.session.commit()
        return {'point': json_point(point)}, 201


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


api.add_resource(PointApi, '/api/points/<point_id>')

api.add_resource(LSTMApi, '/api/lstms/<lstm_id>')

api.add_resource(SaleApi, '/api/sales/<sale_id>')
api.add_resource(ListProductTypesApi, '/api/product_types')


api.add_resource(ListPointsApi, '/api/points')

api.add_resource(ListLSTMsApi, '/api/lstms')
api.add_resource(ListSalesApi, '/api/sales')

#danger(cum) zone
api.add_resource(PredictApi, '/api/predict')


    # data = Sale.query.filter(Sale.shop_id==query['shop_id'], Sale.product_item.product_type_id==query['product_type_id']).all()
        # data = Sale.query.join(ProductItem).filter(Sale.shop_id==query['shop_id'],ProductItem.product_type_id == query['product_type_id']).all()
        # data = ProductItem.query.join(Sale).filter(Sale.shop_id==query['shop_id'],ProductItem.product_type_id == query['product_type_id']).all()
        # data = db.session.query(Sale,ProductItem).filter(Sale.shop_id==query['shop_id'],ProductItem.product_type_id == query['product_type_id']).all()