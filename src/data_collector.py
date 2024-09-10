#!/usr/bin/env python3

from dataclasses import dataclass
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from scout_apm.flask.sqlalchemy import instrument_sqlalchemy
import pika, os

URL = 'https://fakestoreapi.com/products'
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Store.sqlite3'
with app.app_context():
    db.init_app(app)
    instrument_sqlalchemy(db)
AMQPurl = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
params = pika.URLParameters(AMQPurl)
connection = pika.BlockingConnection(params)
search_input = ""
channel = connection.channel()
channel.queue_declare(queue='input')
def callback(ch, method, properties, body):
    set_input(str(body))
channel.basic_consume('input',
                        callback,
                        auto_ack=True)
channel.start_consuming()
connection.close()

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

def set_input(input):
    search_input = input

def return_store():
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