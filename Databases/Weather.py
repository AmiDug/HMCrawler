#!/usr/bin/env python3
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather.sqlite3'

'''
Define the database model
that is used to store 
the temperature.
'''

db = SQLAlchemy(app)


class Weather(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    temperature = db.Column(db.Integer, nullable=False)


'''
Helper function to get temperature
using API
'''


def get_temperature():
    response = requests.get("https://weatherdbi.herokuapp.com/data/weather/boulder")
    return response.json()["currentConditions"]["temp"]["c"]


'''
In main we first get the current temperature and then 
create a new object that we can add to the database. 
'''
if __name__ == "__main__":
    current_temperature = get_temperature()
    new_entry = Weather(temperature=current_temperature)
    db.session.add(new_entry)
    db.session.commit()

'''

Data analysis on endpoint
<start_date> and <end_date>: These are variable parts. 
When a request is made to a URL like /average/2024-08-01/2024-08-15, 
Flask will capture the values 2024-08-01 and 2024-08-15 as the start_date and end_date, 
respectively.

@app.route(average/<start_date>/<end_date>)
def average_temperature():
    sum = 0
    query = db.query(Weather).filter(Weather.date.between(start_date, end_date))
    for item in query:
        sum = sum + item["temp"]
        return sum/query.count()

define route '/metrics' do
    if (application.status == 'running')
        return 200, "Application is healthy"
    else
        return 500, "Application is not healthy"
    end
end


define route '/metrics' do
    totalData = application.dataProcessed
    activePipelines = application.activePipelines
    errorRate = application.errorRate
    return 200, "Data Processed: "+ totalData +", Active Pipelines: "+ activePipelines +", Error Rate: "+ errorRate
end
'''