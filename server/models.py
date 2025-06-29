from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')
    
    items = association_proxy('reviews', 'item',
        creator=lambda item: Review(item=item))
    
    # Serialization rules
    serialize_rules = ('-reviews.customer',)

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    
    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')
    
    customers = association_proxy('reviews', 'customer',
        creator=lambda customer: Review(customer=customer))
    
    # Serialization rules
    serialize_rules = ('-reviews.item',)

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')
    
    # Serialization rules
    serialize_rules = ('-customer.reviews', '-item.reviews',)