""" Module that routes api requests """  # pylint: disable=too-many-lines
import datetime
import hashlib
import pickle
from functools import wraps

import keras.backend.tensorflow_backend as tb
import requests
from flask import request, abort
from flask_restful import Resource

from myapp import api
from myapp.__init__ import db
from myapp.consts import Consts
from myapp.models import ProductType, Point, LSTM, Sale, User, Tag
from myapp.utils import Utils
import utils


def json_type(product_type):
    """Function converts product_type object into dictionary
    :param product_type: (ProductType) Product Type object
    :return dict: dictionary containing converted Product Type
    """
    return {'id': product_type.id, 'name': product_type.name,
            'price': product_type.price,
            'seasonality': product_type.seasonality}


def create_type(query, user_token):
    """ Function creates Product Type from query.
        :param query: (dict) Example: { name:"milk",
                                        price:1000,
                                        seasonality: 0
                                      }
        :return ProductType: Product Type object
    """
    return ProductType(name=query['name'], price=query['price'],
                       seasonality=query['seasonality'], user_token=user_token)


def create_type_with_id(query, product_type_id, user_token):
    """ Function creates Product Type with id from query.
            :param query: (dict) Example: { name:"milk",
                                            price:1000,
                                            seasonality: 0,
                                          }
            :param product_type_id: (int)
            :return ProductType: Product Type object
        """
    return ProductType(id=product_type_id, name=query['name'],
                       price=query['price'], seasonality=query['seasonality'], user_token=user_token)


def json_point(point):
    """ Function converts Point object into dictionary
        :param point: (Point) Point object
        :return dict: dictionary containing converted Point
        """
    return {'id': point.id, 'address': point.address}



def create_point(query, user_token):
    """ Function creates Point from query.
        :param query: (dict) Example: { address: "Moscow" }
        :return Point: Point object
    """
    return Point(address=query['address'], user_token=user_token)


def create_point_with_id(query, point_id, user_token):
    """ Function creates Shop with id from query.
        :param query: (dict) Example: { address: "Moscow" }
        :param shop_id: (int)
        :return Shop: Shop object
    """
    return Point(id=point_id, address=query['address'], user_token=user_token)


def json_lstm(lstm):
    """ Function converts LSTM object into dictionary
        :param lstm: (LSTM) LSTM object
        :return dict: dictionary containing converted LSTM
        """
    return {'id': lstm.id, 'point_id': lstm.point_id,
            'product_type_id': lstm.product_type_id, 'alpha': lstm.alpha,
            'beta': lstm.beta, 'gamma': lstm.gamma, 'prediction': lstm.prediction,
            'before_range': lstm.before_range, 'lstm_pred': lstm.lstm_pred,
            'listForvector': lstm.listForvector, 'realSpros': lstm.realSpros}


def create_lstm(query, user_token):
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
    slen = None
    model_id = None
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
    '''.format(query['point_id'], query[
        'product_type_id'])).fetchall()  # and product_item.product_type_id = {1} and sale.product_item_id = product_item.id
    tb._SYMBOLIC_SCOPE.value = True  # ! костыль
    model = LSTM.query.filter(LSTM.point_id == query['point_id'],
                              LSTM.product_type_id == query['product_type_id']).first()  # +user_id
    if model is None:
        slen = int(ProductType.query.filter(ProductType.id == query['product_type_id']).first().seasonality)
    else:
        slen = model.product_type.seasonality
        before_range = model.before_range
        model_id = model.id
    if 'before_range' in query:
        if before_range != query['before_range']:
            model = None
            before_range = query['before_range']
    alpha, beta, gamma, model, scaler, prediction, before_range, lstm_prediciton = utils.trainModelsAndPredict(data,
                                                                                                               before_range + 1,
                                                                                                               model, slen)  # +1
    step_g = 15

    if alpha == -1:
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
        '''.format(query['point_id'], query['product_type_id'],
                   step_g + 3 if step_g >= before_range else before_range + 3)).fetchall()
        cont_res = utils.predict_step(steps, before_range=before_range + 1, scaler=scaler, model=model)
        spros, list_forvector, real_spros = lstm_prediciton, cont_res[0], cont_res[1]
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
        res_r = utils.predictWinters([row[1] for row in steps], alpha, beta, gamma, slen, step_g)
        spros, list_forvector, real_spros = prediction, res_r[0], res_r[1]

    # print(spros,listForvector,realSpros,before_range,lstm_prediciton,a,b,g)
    return LSTM(id=model_id, point_id=query['point_id'], product_type_id=query[
        'product_type_id'], alpha=alpha, beta=beta,
                gamma=gamma, model=pickle.dumps(model), scope=pickle.dumps(scaler), prediction=prediction,
                lstm_pred=lstm_prediciton, before_range=before_range,
                listForvector=list_forvector, realSpros=real_spros, user_token=user_token)


def create_lstm_with_id(query, lstm_id, user_token):
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
    slen = None
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
    '''.format(query['point_id'], query[
        'product_type_id'])).fetchall()  # and product_item.product_type_id = {1} and sale.product_item_id = product_item.id
    tb._SYMBOLIC_SCOPE.value = True  # ! костыль
    model = LSTM.query.filter(LSTM.id == lstm_id).first()  # +user_id
    if model is None:
        slen = int(ProductType.query.filter(ProductType.id == query['product_type_id']).first().seasonality)
    else:
        slen = model.product_type.seasonality
        before_range = model.before_range
        model_id = model.id
    if 'before_range' in query:
        if before_range != query['before_range']:
            model = None
            before_range = query['before_range']
    alpha, beta, gamma, model, scaler, prediction, before_range, lstm_prediciton = utils.trainModelsAndPredict(data,
                                                                                                               before_range + 1,
                                                                                                               model, slen)
    step_g = 15

    if alpha == -1:
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
        '''.format(query['point_id'], query['product_type_id'],
                   step_g + 3 if step_g >= before_range else before_range + 3)).fetchall()
        cont_res = utils.predict_step(steps, before_range=before_range + 1, scaler=scaler, model=model)
        spros, list_forvector, real_spros = lstm_prediciton, cont_res[0], cont_res[1]
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
        res_r = utils.predictWinters([row[1] for row in steps], alpha, beta, gamma, slen, step_g)
        spros, list_forvector, real_spros = prediction, res_r[0], res_r[1]

    # print(spros,listForvector,realSpros)
    return LSTM(id=lstm_id, point_id=query['point_id'], product_type_id=query[
        'product_type_id'], alpha=alpha, beta=beta,
                gamma=gamma, model=pickle.dumps(model), scope=pickle.dumps(scaler), prediction=prediction,
                lstm_pred=lstm_prediciton, before_range=before_range,
                listForvector=list_forvector, realSpros=real_spros, user_token=user_token)


def json_sale(sale):
    """ Function converts Sale object into dictionary
        :param sale: (Sale) Sale object
        :return dict: dictionary containing converted Sale
    """
    return {'id': sale.id, 'date': str(sale.date),
            'count': sale.count, 'point_id': sale.point_id, 'product_type_id': sale.product_type_id}


def create_sale(query, user_token):
    """ Function creates Sale from query.
        :param query: (dict) Example: { date: '2011-11-04 00:05:23',
                                        product_item_id: 10,
                                        shop_id: 20 }
        :return Sale: Sale object
    """
    return Sale(date=datetime.datetime.fromisoformat(query['date']),
                product_type_id=query['product_type_id'], point_id=query['point_id'],
                count=query['count'], user_token=user_token)


def create_sale_with_id(query, sale_id, user_token):
    """ Function creates Sale with id from query.
        :param query: (dict) Example: { date: '2011-11-04 00:05:23',
                                        product_item_id: 10,
                                        shop_id: 20 }
        :param sale_id: (int)
        :return Sale: Sale object
    """
    return Sale(id=sale_id, date=datetime.datetime.fromisoformat(query['date']),
                product_type_id=query['product_type_id'], point_id=query['point_id'],
                count=query['count'], user_token=user_token)


def json_prediction(prediction):
    """ Function converts Prediction into dictionary
        :param prediction: list[][]
        :return dict: dictionary containing converted prediction
    """
    return {
        'f1': prediction[0][0],
        'f2': prediction[0][1],
        'war_c': prediction[1][0],
        'shop_c': prediction[1][1],
        'war_id': prediction[2][0],
        'shop_id': prediction[2][1],
    }


def make_prediction(query):
    """ Function that creates prediction
        :param TODO
        :return list[][]: predictions list
    """
    tb._SYMBOLIC_SCOPE.value = True  # ! костыль
    models = LSTM.query.filter(LSTM.product_type_id == query['product_type_id']).all()  # пока всё
    full = []
    for i in models:
        full.append({'spros': i.lstm_pred if i.alpha == -1 else i.prediction,
                     'shop': Point.query.filter(Point.id == i.point_id).first(),
                     'listForvector': i.listForvector, 'realSpros': i.realSpros, 'price': i.product_type.price})

    return utils.main_prediction(full)


def create_user(name, email, password_hash, token, privilege_level=1):
    """ Function creates User from query.
        :param name: (string)
        :param email: (string)
        :param password_hash: (string)
        :param privilege_level: (int)
        :param token: (string)
    """
    return User(name=name, email=email, password_hash=password_hash, privilege_level=privilege_level, token=token)


def json_tag(tag):
    """ Function converts Tag object into dictionary
        :param tag: (Tag) Tag object
        :return dict: dictionary containing converted Tag
    """
    return {'id': tag.id, 'minimum': tag.minimum, 'capacity': tag.capacity, 'fullness': tag.fullness }


def create_tag(query, user_token):
    """ Function creates Tag from query.
        :param query: (dict) Example: {
                                          "minimum": 10,
                                          "capacity": 200
                                          "fulness": 10
                                      }
        :return Tag: Tag object
    """
    return Tag(minimum=query['minimum'], capacity=query['capacity'], fulness=query['fullness'], user_token=user_token)


def create_tag_with_id(query, tag_id, user_token):
    """ Function creates Tag with id from query.
        :param query: (dict) Example: {
                                          "minimum": 10,
                                          "capacity": 50,
                                          "fulness": 10
                                      }
        :param tag_id: (int)
        :return Tag: Tag object
    """
    return Tag(id=tag_id, minimum=query['minimum'], capacity=query['capacity'], fulness=query['fullness'], user_token=user_token)


def require_authentication(func):
    """ Annotation requires token

        @require_api_token
        def sample_method(user):
            return {"Hey, " + user.name + ", you are authenticated!"}

    """

    @wraps(func)
    def check_token(*args, **kwargs):
        user = None

        if not 'Authorization' in request.headers:
            invalid_token = True
        else:
            token = request.headers['Authorization']
            user = User.query.filter(User.token == token).first()
            invalid_token = user is None

        if invalid_token:
            return {"message": "Invalid token."}, 999

        return func(*args, **kwargs, user=user)

    return check_token


class ListProductTypesApi(Resource):
    """ Class that gets all Product Types or creates new """

    @staticmethod
    @require_authentication
    def get(user):
        """ Method used to get list of all Product Types
            :return: list[ProductType]
        """

        product_types = ProductType.query.filter(ProductType.user_token == user.token).all()
        return {'product_types': [json_type(product_type) for product_type in product_types]}, 200

    @staticmethod
    @require_authentication
    def post(user):
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
        product_type = create_type(request.json, user.token)
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
    @require_authentication
    def put(product_type_id, user):
        """ Update/Create Product Type by id
            :param product_type_id: (int)
            :return: ProductType: Product Type object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(ProductType.query.get_or_404(product_type_id))
        db.session.commit()
        product_type = create_type_with_id(request.json, product_type_id, user.token)
        db.session.add(product_type)
        db.session.commit()
        return {'product_type': json_type(product_type)}, 201


class ListPointsApi(Resource):
    """ Class that gets all Shops or creates new """

    @staticmethod
    @require_authentication
    def get(user):
        """ Method used to get list of all Shops
            :return: list[Shop]
        """
        points = Point.query.filter(Point.user_token == user.token).all()
        return {'points': [json_point(points) for points in points]}, 200

    @staticmethod
    @require_authentication
    def post(user):
        """ Create new Shop
            Example shop post query:
            {
                "address": "Moscow"
            }
            :return: jsonifyed Shop
        """
        if not request.json:
            abort(400, "No data")
        point = create_point(request.json, user.token)
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
    @require_authentication
    def put(point_id, user):
        """ Update/Create Shop by id
            :param shop_id: (int)
            :return: Shop: Shop object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(Point.query.get_or_404(point_id))
        db.session.commit()
        point = create_point_with_id(request.json, point_id, user.token)
        db.session.add(point)
        db.session.commit()
        return {'point': json_point(point)}, 201


class ListLSTMsApi(Resource):
    """ Class that gets all LSTMs or creates new """

    @staticmethod
    @require_authentication
    def get(user):
        """ Method used to get list of all LSTMs
            :return: list[LSTM]
        """
        lstms = LSTM.query.filter(LSTM.user_token == user.token).all()
        return {'LSTMs': [json_lstm(lstm) for lstm in lstms]}, 200

    @staticmethod
    @require_authentication
    def post(user):
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
        lstm = create_lstm(request.json, user.token)
        if lstm.id is not None:
            db.session.delete(LSTM.query.get_or_404(lstm.id))
            db.session.commit()
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
    @require_authentication
    def put(lstm_id, user):
        """ Update/Create LSTM by id
            :param lstm_id: (int)
            :return: LSTM: LSTM object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(LSTM.query.get_or_404(lstm_id))
        db.session.commit()
        lstm = create_lstm_with_id(request.json, lstm_id, user.token)
        db.session.add(lstm)
        db.session.commit()
        return {'lstm': json_lstm(lstm)}, 201


class ListSalesApi(Resource):
    """ Class that gets all Sales or creates new """

    @staticmethod
    @require_authentication
    def get(user):
        """ Method used to get list of all Sales
            :return: list[Sale]
        """
        sales = Sale.query.filter(Sale.user_token == user.token).all()
        return {'sales': [json_sale(sales) for sales in sales]}, 200

    @staticmethod
    @require_authentication
    def post(user):
        """ Create new Sale
            Example sale post query:
            {
                "date": "2011-11-04 00:05:23",
                "product_item_id": 10,
                "shop_id": 20
            }
            :return: jsonifyed Sale
        """
        if not request.json:
            abort(400, "No data")
        sale = create_sale(request.json, user.token)
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
    @require_authentication
    def put(sale_id, user):
        """ Update/Create Sale by id
            :param sale_id: (int)
            :return: Sale: Sale object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(Sale.query.get_or_404(sale_id))
        db.session.commit()
        sale = create_sale_with_id(request.json, sale_id, user.token)
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
        predictions = make_prediction(request.json)
        print(predictions)
        return {'predictions': [json_prediction(prediction) for prediction in predictions]}, 200


class ListTagsApi(Resource):
    """ Class that gets all Tags or creates new """

    @staticmethod
    @require_authentication
    def get(user):
        """ Method used to get list of all Tags
            :return: list[Tag]
        """

        tags = Tag.query.filter(Tag.user_token == user.token).all()
        return {'tags': [json_tag(tag) for tag in tags]}, 200

    @staticmethod
    @require_authentication
    def post(user):
        """ Create new Tag
            Example tag post query:
            {
                "minimum": 10,
                "capacity": 200
            }
            :return: jsonifyed Tag
        """
        if not request.json:
            abort(400, "No data")
        tag = create_tag(request.json, user.token)
        db.session.add(tag)
        db.session.commit()
        return {'tag': json_tag(tag)}, 201


class TagsApi(Resource):
    """ Class that gets/updates/deletes Tags by id """

    @staticmethod
    def get(tag_id):
        """ Get Tags by id
            :param tag_id: (int)
            :return Tags: Tag object
        """
        tag = Tag.query.get_or_404(tag_id)
        return {'tag': json_tag(tag)}, 200

    @staticmethod
    def delete(tag_id):
        """ Deletes Tag by id
            :param tag_id: (int)
            :return: empty html
        """
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return "", 200

    @staticmethod
    @require_authentication
    def put(tag_id, user):
        """ Update/Create Tag by id
            :param tag_id: (int)
            :return: Tag: Tag object
        """
        if not request.json:
            abort(400, "No data")
        db.session.delete(Tag.query.get_or_404(tag_id))
        db.session.commit()
        tag = create_tag_with_id(request.json, tag_id, user.token)
        db.session.add(tag)
        db.session.commit()
        return {'tag': json_tag(tag)}, 201



class AuthenticationApi(Resource):
    """ Class that allows to authenticate (sign in && sign up) """

    @staticmethod
    def get():
        """ Method used to sign in
            Example of query:
            {
                "name": "Tester",
                "password": "qwerty123",
                "remember": "true"
            }
            :return: list[]
        """

        name = request.args.get('name')
        password = request.args.get('password')
        password_hash = hashlib.md5(password.encode() + Consts.PASSWORD_SALT).hexdigest()

        user = User.query.filter(User.name == name, User.password_hash == password_hash).first()

        if user is not None:
            return {'is_success': True, 'name': user.name, 'token': user.token}

        return {'is_success': False}

    @staticmethod
    def post():
        """ Method used to sign up
            Example of query:
            {
                "name": "Tester",
                "password": "qwerty123",
                "email": "tester@ya.ru"
            }
            :return: list[]
        """

        request_json = request.json

        if not request_json:
            return abort(400, "No data")

        errors = []

        name = request_json["name"]
        email = request_json["email"]
        password = request_json["password"]
        password_repeat = request_json["password_repeat"]

        if len(name) < 5 or len(name) > 12:
            errors.append('Name must be greater than 5 chars and less than 12 chars')

        if db.session.query(User.query.filter(User.name == name).exists()).scalar():
            errors.append('Name is already taken')

        if not Utils.is_email_valid(email):
            errors.append('Email is invalid')

        if len(password) < 6:
            errors.append('Password must be greater than 6 chars')

        if password != password_repeat:
            errors.append('Password repeat is invalid')

        if len(errors) > 0:
            return {'is_success': False, "error": errors[0]}

        password_hash = hashlib.md5(password.encode() + Consts.PASSWORD_SALT).hexdigest()
        privilege_level = 1
        token = hashlib.sha256((name + Utils.random_string(10)).encode()).hexdigest()

        user = create_user(name, email, password_hash, token, privilege_level)
        db.session.add(user)
        db.session.commit()

        return {'is_success': True, 'name': name, 'token': token}


class IntegrateUserApi(Resource):
    """ Class that integrates user with moysklad.ru """

    @staticmethod
    @require_authentication
    def post(user):
        """ Method that integrates user with moysklad.ru
            Example of query:
            {
                "moysklad_password": "1231231",
                "moysklad_login": "abc@def"
            }
            :return: list[]
        """
        if not request.json:
            return abort(400, "No data")
        request_json = request.json
        user.moysklad_login = request_json['moysklad_login']
        user.moysklad_password = request_json['moysklad_password']
        response = requests.get('https://online.moysklad.ru/api/remap/1.1/entity/move?expand=positions',
                                auth=requests.auth.HTTPBasicAuth(user.moysklad_login, user.moysklad_password))
        user.moysklad_id = response.json()['rows'][0]['accountId']
        db.session.add(user)
        db.session.commit()
        return {'is_success': True}


class IntegrateApi(Resource):
    """ Class that imports data from moysklad.ru """

    @staticmethod
    @require_authentication
    def post(user):
        """ Method that imports all data from moysklad.ru """
        response = requests.get('https://online.moysklad.ru/api/remap/1.1/entity/product',
                                auth=requests.auth.HTTPBasicAuth(user.moysklad_login, user.moysklad_password))
        for item in response.json()['rows']:
            product_type_id = item['id']
            name = item['name']
            price = item['salePrices'][0]['value']
            product_type = ProductType(id=product_type_id, name=name, user_token=user.token, price=price, seasonality=0, tag_id=1)
            db.session.add(product_type)
        products_count = len(response.json()['rows'])
        response = requests.get('https://online.moysklad.ru/api/remap/1.1/entity/store',
                                auth=requests.auth.HTTPBasicAuth(user.moysklad_login, user.moysklad_password))
        for item in response.json()['rows']:
            point_id = item['id']
            address = item['address']
            point = Point(id=id, address=address, user_token=user.token)
            db.session.add(point)
        db.session.commit()
        response = requests.get('https://online.moysklad.ru/api/remap/1.1/report/stock/bystore',
                                auth=requests.auth.HTTPBasicAuth(user.moysklad_login, user.moysklad_password))
        for index, item in enumerate(response.json()['rows']):
            for store_item in item['stockByStore']:
                point_id = store_item['meta']['href'].split('/')[-1]
                product_type_id = item['meta']['href'].split('/')[-1].split('?')[0]
                tag = Tag(point_id=point_id, product_type_id=product_type_id, minimum=0, capacity=1000, fullness=store_item['stock'])
                db.session.add(tag)
                db.session.commit()
        db.session.commit()
        shops_list = set()
        response = requests.get(
            'https://online.moysklad.ru/api/remap/1.1/entity/retaildemand?expand=positions.demandposition,positions.assortment.product,store',
            auth=requests.auth.HTTPBasicAuth(user.moysklad_login, user.moysklad_password))
        for item in response.json()['rows']:
            sale_id = item['id']
            date = datetime.datetime.fromisoformat(item['updated'])
            point_id = item['store']['id']
            shops_list.add(point_id)
            for position in item['positions']['rows']:
                count = position['quantity']
                product_type_id = position['assortment']['id']
                price = position['price']
                sale = Sale(id=sale_id, date=date, point_id=point_id, count=count,
                            product_type_id=product_type_id, price=price, user_token=user.token)
                db.session.add(sale)
        db.session.commit()
        # если мыразличаем склады и магазины то код дальше не нужен
        response = requests.get('https://online.moysklad.ru/api/remap/1.1/entity/move?expand=positions',
                                auth=requests.auth.HTTPBasicAuth(user.moysklad_login, user.moysklad_password))
        for item in response.json()['rows']:
            point_id = item['sourceStore']['meta']['href'].split('/')[-1]
            if not point_id in shops_list:
                sale_id = item['id']
                date = datetime.datetime.fromisoformat(item['updated'])
                for position in item['positions']['rows']:
                    count = position['quantity']
                    product_type_id = position['assortment']['id']
                    price = position['price']
                    sale = Sale(id=sale_id, date=date, point_id=point_id, count=count,
                                product_type_id=product_type_id, price=price, user_token=user.token)
                    db.session.add(sale)
        db.session.commit()
        return "ok", 200


api.add_resource(IntegrateApi, '/api/user/integrate')
api.add_resource(IntegrateUserApi, '/api/authentication/integrate')
api.add_resource(AuthenticationApi, '/api/authentication')
api.add_resource(ProductTypesApi, '/api/product_types/<product_type_id>')
api.add_resource(PointApi, '/api/points/<point_id>')
api.add_resource(LSTMApi, '/api/lstms/<lstm_id>')
api.add_resource(SaleApi, '/api/sales/<sale_id>')
api.add_resource(TagsApi, '/api/tags/<tag_id>')
api.add_resource(ListProductTypesApi, '/api/product_types')
api.add_resource(ListPointsApi, '/api/points')
api.add_resource(ListLSTMsApi, '/api/lstms')
api.add_resource(ListSalesApi, '/api/sales')
api.add_resource(PredictApi, '/api/predict')
api.add_resource(ListTagsApi, '/api/tags')
