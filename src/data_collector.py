#!/usr/bin/env python3

import requests
from dataclasses import dataclass
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scout_apm.flask.sqlalchemy import instrument_sqlalchemy

URL = 'https://fakestoreapi.com/products'
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Store.sqlite3'
with app.app_context():
    db.init_app(app)
    instrument_sqlalchemy(db)

@dataclass
class Store(db.Model):
    """
    Define the database model
    that is used to store
    the temperature.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    category = db.Column(db.String)
    image = db.Column(db.String)
    rate = db.Column(db.Float)
    count = db.Column(db.Integer)

with app.app_context():
    inspector = db.inspect(db.engine)
    if 'store' not in inspector.get_table_names():
        db.drop_all()
        db.create_all()

def fetch_store():
    """
    Fetch data from a fake store API and return it as JSON data
    :rtype: object
    """
    try:
        response = requests.get(URL)
    except ValueError as err:
        print("An exception occurred:", type(err).__name__)
    return response.json()

def populate_db():
    """
    In main we first get the current temperature and then
    create a new object that we can add to the database.
    :rtype: object
    """
    store_values = fetch_store()
    with app.app_context():
        for item in store_values:
            existing_product = Store.query.get(item['id'])
            if existing_product is None:
                new_entry = Store(
                    id=item['id'],
                    title=item['title'],
                    price=item['price'],
                    description=item['description'],
                    category=item['category'],
                    image=item['image'],
                    rate=item['rating']['rate'],
                    count=item['rating']['count'])
                db.session.add(new_entry)
            db.session.commit()

def return_store(search_input):
    """
    Queries the database using user input and outputs all items that match as a list.
    :rtype: object
    """
    with app.app_context():
        store_values = Store.query.filter(Store.title.contains(search_input))
        store_list = []
        for item in store_values:
            item_data = {
                'id': item.id,
                'title': item.title,
                'price': item.price,
                'description': item.description,
                'category': item.category,
                'image': item.image,
                'rate': item.rate,
                'count': item.count
            }
            store_list.append(item_data)
        return store_list