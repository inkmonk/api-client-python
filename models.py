from flask.ext.security import SQLAlchemyUserDatastore, UserMixin, RoleMixin
import json
import uuid
from datetime import datetime
from model_helpers import Serializer, monetize
from decimal import Decimal, ROUND_UP, ROUND_DOWN
from dblayer import db
from flask.ext.sqlalchemy import orm

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.String(40), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


def date_serial(value):
    return value.strftime("%Y-%m-%d") + " " + value.strftime("%H:%M:%S")


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Template(db.Model):
    __tablename__ = 'templates'
    id = db.Column(db.String(40), primary_key=True)
    type = db.Column(db.String(100))
    dimension = db.Column(db.String(20))
    created_at = db.Column(db.DateTime())

    def __init__(self, id=None, type=None, dimension=None):
        self.id = id or uuid.uuid4().hex
        self.type = type
        self.dimension = dimension
        self.created_at = datetime.utcnow().isoformat()

    def update(self, **kwargs):
        columns = self.__table__.columns.keys()
        for key, value in kwargs:
            if key in columns and (key not in self.__no_overwrite__):
                setattr(self, key, value)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())

    def __repr__(self):
        return self.type + " - " + self.dimension


class TemplatePriceSlab(db.Model):
    __tablename__ = 'template_price_slabs'
    id = db.Column(db.String(40), primary_key=True)
    template_id = db.Column(db.String(40), db.ForeignKey('templates.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric)

    template = db.relationship("Template", backref=db.backref("price_slabs", cascade="all, delete-orphan"))

    def __init__(self, id=None, template_id=None, quantity=None, price=None):
        self.id = id or uuid.uuid4().hex
        self.template_id = template_id
        self.quantity = quantity
        self.price = Decimal(price).quantize(Decimal('.01'), rounding=ROUND_UP)

    def update(self, **kwargs):
        columns = self.__table__.columns.keys()
        for key, value in kwargs.items():
            if key in columns and (key not in self.__no_overwrite__):
                setattr(self, key, value)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())

    @property
    def total_cost(self):
      return monetize(self.price * self.quantity)

    def __repr__(self):
        return self.template.type + " - " + self.template.dimension + " - " + str(self.quantity)


class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)


class PincodeDetail(db.Model):
    __tablename__ = 'pincode_details'

    id = db.Column(db.Integer, primary_key=True)
    pincode = db.Column(db.Integer, nullable=False, unique=True)
    city = db.Column(db.String(40))
    state = db.Column(db.String(40))
    bluedart_prepaid = db.Column(db.Boolean)
    dotzot_prepaid = db.Column(db.Boolean)
    professional = db.Column(db.Boolean)
    bluedart_zone = db.Column(db.String(16))


class Order_Product(db.Model, Serializer):
    __tablename__ = 'orders_products'
    __public__ = ['id', 'order_id', 'product_id', 'quantity']

    id = db.Column(db.String(40), primary_key=True, unique=True)
    order_id = db.Column(db.String(40), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(40), db.ForeignKey('products.id'), nullable=False)
    template_price_slab_id = db.Column(db.String(40), db.ForeignKey('template_price_slabs.id'), nullable=False)
    quantity = db.Column(db.Integer)
    amount = db.Column(db.Numeric)

    order = db.relationship("Order", backref=db.backref("order_product_assoc", cascade="all, delete-orphan"))
    product = db.relationship("Product", backref=db.backref("order_product_assoc", cascade="all, delete-orphan"))
    template_price_slab = db.relationship("TemplatePriceSlab", backref="order_product_assoc")

    def __init__(self, id=None, order_id=None, product_id=None, template_price_slab_id=None, quantity=None, amount=None ):
        self.id = id or uuid.uuid4().hex
        self.order_id = order_id
        self.product_id = product_id
        self.template_price_slab_id=template_price_slab_id
        self.quantity = quantity or db.session.query(TemplatePriceSlab).get(self.template_price_slab_id).quantity
        self.amount = amount or db.session.query(TemplatePriceSlab).get(self.template_price_slab_id).total_cost

    def update(self, **kwargs):
        columns = self.__table__.columns.keys()
        for key, value in kwargs.items():
            if key in columns and (key not in self.__no_overwrite__):
                setattr(self, key, value)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())


class Product(db.Model, Serializer):
    __tablename__ = 'products'

    # Fields that appear in serialized model
    __public__ = ['id', 'name', 'design_file',
                  'design_status', 'template_id',
                  'quantity', 'created_at', 'user_id']

    # Fields that cannot be updated
    __no_overwrite__ = ['id', 'created_at', 'user_id', 'template_id']

    id = db.Column(db.String(40), primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    design_file = db.Column(db.String(100), nullable=False)
    design_status = db.Column(db.String(50), default="pending", nullable=False)
    translucent = db.Column(db.Boolean, default=False)
    template_id = db.Column(db.String(40), db.ForeignKey('templates.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(40), db.ForeignKey('users.id'))

    orders = db.relationship("Order", secondary="orders_products", viewonly=True)
    template = db.relationship("Template", backref=db.backref("products", cascade="all, delete-orphan"))

    #order_product_assoc = db.relationship('Order_Product', backref='product', primaryjoin=id == Order_Product.product_id)

    def __init__(self, id=None, name=None, design_file=None, design_status="pending", translucent=False, template_id=None, quantity=None, user_id=None):
        self.id = id or uuid.uuid4().hex
        self.name = name
        self.design_file = design_file
        self.design_status = design_status
        self.translucent = translucent
        self.template_id=template_id
        self.created_at = datetime.utcnow().isoformat()
        self.user_id = user_id


    def update(self, **kwargs):
        columns = self.__table__.columns.keys()
        for key, value in kwargs.items():
            if key in columns and (key not in self.__no_overwrite__):
                setattr(self, key, value)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())


class Customer(db.Model, Serializer):
    __tablename__ = 'customers'
    __public__ = ['id', 'name', 'email', 'phone_number',
                  'address1', 'address2', 'city', 'state',
                  'country', 'pincode', 'user_id']

    __no_overwrite__ = ['id', 'user_id']

    id = db.Column(db.String(40), primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    address1 = db.Column(db.String(100), nullable=False)
    address2 = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(20))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(40), db.ForeignKey('users.id'))

    @property
    def address(self):
        return self.address1+" , "+self.address2+" , "+self.city+" , "+self.state+" , "+str(self.pincode)

    def __init__(self, id=None, name=None, email=None, phone_number=None, address1=None, address2=None, city=None, state=None, country=None, pincode=None, user_id=None):
        self.id = id or uuid.uuid4().hex
        self.name = name
        self.phone_number = phone_number
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.country = country
        self.pincode = pincode
        self.user_id = user_id
        self.email = email

    def update(self, **kwargs):
        columns = self.__table__.columns.keys()
        for key, value in kwargs.items():
            if key in columns and (key not in self.__no_overwrite__):
                setattr(self, key, value)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())


class Order(db.Model, Serializer):
    __tablename__ = 'orders'
    __public__ = ['id', 'amount', 'customer_id', 'created_at'
                  'delivery_date', 'status', 'tracking_url',
                  'package_cover_id', 'products']
    __no_overwrite__ = ['id', 'created_at']

    id = db.Column(db.String(40), primary_key=True, unique=True)
    amount = db.Column(db.Numeric, default=0.00)
    customer_id = db.Column(db.String(35), db.ForeignKey('customers.id'))
    package_cover_id = db.Column(db.String(50))
    created_at = db.Column(db.String(50), nullable=False)
    delivery_date = db.Column(db.String(50))
    status = db.Column(db.String(20), default='processing', nullable=False)
    tracking_url = db.Column(db.String(512))
    user_id = db.Column(db.String(50), db.ForeignKey('users.id'))
    sku = db.Column(db.String(50))
    courier_provider = db.Column(db.String(50))

    #order_product_assoc = db.relationship('Order_Product', backref='order', primaryjoin=id == Order_Product.order_id)

    products = db.relationship("Product", secondary="orders_products", viewonly=True)

    customer = db.relationship("Customer", backref="orders")


    @property
    def customer_name(self):
        return self.customer.name

    def __init__(self, id=None, amount=0, customer_id=None, package_cover_id=None, delivery_date=None, tracking_url=None, user_id=None, sku=None):
        self.id = id or uuid.uuid4().hex
        self.created_at = datetime.utcnow().isoformat()
        self.amount = amount
        self.customer_id = customer_id
        self.package_cover_id = package_cover_id
        self.delivery_date = delivery_date
        self.tracking_url = tracking_url
        self.user_id = user_id
        self.sku = sku

    def add_products(self, items=[], id_list=[]):
        """ Method to add products to an order

        Arguments:

        items: list of tuples of product object and template_price_slab_id
        id_list: list of tuples of product id and template_price_slab_id
        """
        try:
            assocs=[]
            if not id_list:
                for product, template_price_slab_id in items:
                    if product.user_id == self.user_id:
                        assoc = Order_Product(order_id=self.id,
                                              product_id=product.id,
                                              template_price_slab_id=template_price_slab_id)
                        self.amount+=monetize(db.session.query(TemplatePriceSlab).get(template_price_slab_id).price)
                        assocs.append(assoc)
            else:
                for id, template_price_slab_id in id_list:
                    product = db.session.query(Product).filter_by(id=id).one()
                    if product.user_id == self.user_id:
                        assoc = Order_Product(order_id=self.id,
                                              product_id=id,
                                              template_price_slab_id=template_price_slab_id)
                        self.amount+=monetize(db.session.query(TemplatePriceSlab).get(template_price_slab_id).price)
                        assocs.append(assoc)
            db.session.add_all(assocs)
            db.session.commit()
        except Exception as e:
                print e
                raise

    def update(self, **kwargs):
        columns = self.__table__.columns.keys()
        for key, value in kwargs.items():
            if key in columns and (key not in self.__no_overwrite__):
                setattr(self, key, value)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __public__ = ['id', 'api_key', 'email', 'password',
                  'type', 'phone_number', 'customers', 'products']

    #
    # Note: 'products' added here to enable explicit updating
    # of products using add_products() and not via update()
    #
    __no_overwrite__ = ['id', 'secret_access_key', 'products']

    id = db.Column(db.String(40), primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(255))
    name = db.Column(db.String(50))
    type = db.Column(db.String(20))
    active = db.Column(db.Boolean())
    phone_number = db.Column(db.Integer)
    confirmed_at = db.Column(db.DateTime())
    api_key = db.Column(db.String(255))
    secret_access_key = db.Column(db.String(255))

    customers = db.relationship('Customer', order_by='Customer.id', backref='user', cascade="all, delete, delete-orphan")
    products = db.relationship('Product', order_by='Product.id', backref='user', cascade="all, delete, delete-orphan")
    orders = db.relationship('Order', order_by='Order.id', backref='user', cascade="all, delete, delete-orphan")

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, id=None,  name=None, email=None, password=None, type=None, phone_number=None, roles=[], active=None):
        self.id = id or uuid.uuid4().hex
        self.created_at = datetime.utcnow().isoformat()
        self.name = name
        self.email = email
        self.password = password
        self.type = type
        self.phone_number = phone_number
        self.api_key = uuid.uuid4().hex
        self.secret_access_key = uuid.uuid4().hex
        self.active = active
        self.roles = roles

    def update(self, **kwargs):
        columns = self.__table__.columns.keys()
        for key, value in kwargs.items():
            if key in columns and (key not in self.__no_overwrite__):
                setattr(self, key, value)

    def to_json(self):
        return json.dumps(self.to_serializable_dict())

    def has_role(self, role):
        if not isinstance(role, Role):
            role=db.session.query(Role).filter_by(name=role).first()
        return role in self.roles

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#security = Security(app, user_datastore)
