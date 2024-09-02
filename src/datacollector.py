#!/usr/bin/env python3

from dataclasses import dataclass
import requests, json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

URL = 'https://fakestoreapi.com/products'
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Store.sqlite3'
with app.app_context():
    db.init_app(app)

'''
Define the database model
that is used to store 
the temperature.
'''

@dataclass
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    category = db.Column(db.String)
    image = db.Column(db.String)
    rate = db.Column(db.Float)
    count = db.Column(db.String)

with app.app_context():
    db.create_all()

'''
fetch data from a fake store API and return it as JSON data
'''
def fetch_store():
    response = requests.get(URL)
    #response = json.dumps(response.text)
    return response.json() #return response.json()["currentConditions"]["temp"]["c"]

'''
In main we first get the current temperature and then 
create a new object that we can add to the database. 
'''
def populate_db():
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

def return_store():
    with app.app_context():
        store_values = Store.query.all()
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
        return {'products': store_list}

'''
Sure! Let’s break down the code snippet return response.json()["currentConditions"]["temp"]["c"]:

response.json(): This method converts the JSON response from an API call into a Python dictionary. JSON (JavaScript Object Notation) is a common format for sending data in web applications.
["currentConditions"]: This accesses the value associated with the key "currentConditions" in the dictionary. This key likely contains another dictionary with various weather-related data.
["temp"]: This accesses the value associated with the key "temp" within the "currentConditions" dictionary. This key likely holds temperature data.
["c"]: This accesses the value associated with the key "c" within the "temp" dictionary. This key likely represents the temperature in Celsius.
So, the entire line of code retrieves the current temperature in Celsius from the JSON response and returns it.
'''