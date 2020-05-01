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
        tags: 1, 2
        product_items: ProductItem1, ProductItem2
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    tags = db.relationship('Tag', secondary=TAGS,
                           backref=db.backref('product_types', lazy='dynamic'),
                           lazy='dynamic')
    product_items = db.relationship('ProductItem', backref='product_type',
                                    lazy='dynamic')


class ProductItem(db.Model):  # pylint: disable=too-few-public-methods
    """ Class that contains Product Item, connected with Product Type,
    Product Groups.
        Example:
            id: 1
            count: 10
            product_type: ProductType1
            product_type_id: 1
            product_group: ProductGroup1
            product_group_id: 1
    """
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
    product_group_id = db.Column(db.Integer, db.ForeignKey('product_group.id'))


class ProductGroup(db.Model):  # pylint: disable=too-few-public-methods
    """ Class that contains Product Group, connected with Product Items.
        Example:
            id: 1
            product_items: ProductItem1, ProductItem2
    """
    id = db.Column(db.Integer, primary_key=True)
    product_items = db.relationship('ProductItem', backref='product_group',
                                    lazy='dynamic')


class Location(db.Model):  # pylint: disable=too-few-public-methods
    """ Class that contains Location.
    Example:
        address: Yubileynaya Street, 13/2
        latitude: 55.911905
        longitude: 37.719328
    """
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
