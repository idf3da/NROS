"""
Module contains SQLAlchemy-based ORM
"""
from myapp import db

TAGS = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('page_id', db.Integer,
                          db.ForeignKey('product_type.id'))
                )


class Tag(db.Model):  # pylint: disable=too-few-public-methods
    """ Class that contains Tag, connected with Product Types.
    Example:
        id: 1
        product_types: ProductType1, ProductType2
    """
    id = db.Column(db.Integer, primary_key=True)


class ProductType(db.Model):  # pylint: disable=too-few-public-methods
    """ Class that contains Product Type, connected with Tags, Product Items.
    Example:
        id: 1
        name: Milk
        price: 1000
        seasonality: 10
        product_items: ProductItem1, ProductItem2
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    seasonality = db.Column(db.Integer)
    tags = db.relationship('Tag', secondary=TAGS,
                           backref=db.backref('product_types', lazy='dynamic'),
                           lazy='dynamic')
    # product_items = db.relationship('ProductItem', backref='product_type',
                                    # lazy='dynamic')
    lstms = db.relationship('LSTM', backref='product_type', lazy='dynamic')


# class ProductItem(db.Model):  # pylint: disable=too-few-public-methods
#     """ Class that contains Product Item, connected with Product Type,
#     Product Groups.
#         Example:
#             id: 1
#             count: 10
#             product_type: ProductType1
#             product_type_id: 1
#             product_group: ProductGroup1
#             product_group_id: 1
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     count = db.Column(db.Integer)
#     # product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
#     # product_group_id = db.Column(db.Integer, db.ForeignKey('product_group.id'))
#     # sale = db.relationship('Sale', backref='product_item', lazy='dynamic')


# class ProductGroup(db.Model):  # pylint: disable=too-few-public-methods
#     """ Class that contains Product Group, connected with Product Items.
#         Example:
#             id: 1
#             product_items: ProductItem1, ProductItem2
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     product_items = db.relationship('ProductItem', backref='product_group',
#                                     lazy='dynamic')


# class Location(db.Model):  # pylint: disable=too-few-public-methods
#     """ Class that contains Location.
#     Example:
#         address: Yubileynaya Street, 13/2
#         latitude: 55.911905
#         longitude: 37.719328
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String(100))
#     latitude = db.Column(db.Float())
#     longitude = db.Column(db.Float())
#     shops = db.relationship('Shop', backref='location', lazy='dynamic')
#     warehouses = db.relationship('Warehouse', backref='location',
#                                  lazy='dynamic')

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    fullness = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    minimum = db.Column(db.Integer)
    shop = db.Column(db.Boolean)
    shop_id = db.Column(db.ARRAY(db.Integer))
    lstms = db.relationship('LSTM', backref='point', lazy='dynamic')
    sales = db.relationship('Sale', backref='shop', lazy='dynamic')
class User(db.Model):
    """ Class that contains User."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password_hash = db.Column(db.String)
    email = db.Column(db.String)
    privilege_level = db.Column(db.Integer)
    token = db.Column(db.String)
# class Shop(db.Model):  # pylint: disable=too-few-public-methods
#     """ Class that contains Shop(Retail Point)"""
#     id = db.Column(db.Integer, primary_key=True)
#     location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
#     lstms = db.relationship('LSTM', backref='shop', lazy='dynamic')
#     fullness = db.Column(db.Integer)
#     capacity = db.Column(db.Integer)
#     sales = db.relationship('Sale', backref='shop', lazy='dynamic')
#     # minimum = db.Column(db.Integer)
#     # warehouse = db.relationship('Warehouse')

# class Warehouse(db.Model):  # pylint: disable=too-few-public-methods
#     """ Class that contains Warehouse"""
#     id = db.Column(db.Integer, primary_key=True)
#     location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
#     fullness = db.Column(db.Integer)
#     capacity = db.Column(db.Integer) 
#     # shops = db.relationship("Shop", backref="warehouse", lazy='dynamic')

class Sale(db.Model):  # pylint: disable=too-few-public-methods
    """ Class that contains ProductItem Sale """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)  # python datetime.datetime() object
    # product_item_id = db.Column(db.Integer, db.ForeignKey('product_item.id'))
    point_id = db.Column(db.Integer, db.ForeignKey('point.id'))
    # product_item = db.relationship("ProductItem",backref="classes")
    count = db.Column(db.Integer)
    
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id')) #сука надо добавить я заебался писать через product_item


class LSTM(db.Model):  # pylint: disable=too-few-public-methods
    """ Class that contains LSTM."""
    id = db.Column(db.Integer, primary_key=True)
    point_id = db.Column(db.Integer, db.ForeignKey('point.id'))
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
    alpha = db.Column(db.Float)
    beta = db.Column(db.Float)
    gamma = db.Column(db.Float)
    model = db.Column(db.PickleType)
    scope = db.Column(db.PickleType)
    prediction = db.Column(db.Integer)
    before_range = db.Column(db.Integer)
    lstm_pred = db.Column(db.Integer)
    listForvector = db.Column(db.ARRAY(db.Integer))
    realSpros = db.Column(db.ARRAY(db.Integer))