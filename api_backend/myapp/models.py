from myapp import db

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('page_id', db.Integer,
                          db.ForeignKey('product_type.id'))
                )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class ProductType(db.Model):
    # singletone object:
    # Молоко, Домик в деревне, 100 бурлей, 1л, молочные продукты
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    volume = db.Column(db.Integer)
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('product_types', lazy='dynamic'),
                           lazy='dynamic')
    product_items = db.relationship('ProductItem', backref='product_type',
                                    lazy='dynamic')


class ProductItem(db.Model):  # Молоко: 2 шт.
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
    product_group_id = db.Column(db.Integer, db.ForeignKey('product_group.id'))


class ProductGroup(db.Model):  # [Молоко: 2шт, Кефир: 3шт]
    id = db.Column(db.Integer, primary_key=True)
    product_items = db.relationship('ProductItem', backref='product_group',
                                    lazy='dynamic')


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    '''
    надо подумать как мы будем реализовывать локацию
    '''


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    storage_capacity = db.Column(db.Integer)


class Warehouse(Property, db.Model):
    """
    не знаю будет ли он чем то отличаться в модели
    """


class RetailPoint(Property, db.Model):
    """
        не знаю будет ли он чем то отличаться в модели
    """
