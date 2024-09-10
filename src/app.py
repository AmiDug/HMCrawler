#!/usr/bin/env python3

from flask import Flask, request, render_template
from src.data_collector import return_store, populate_db
from src.data_analyzer import return_count_average, return_price_average, return_rating_average
from scout_apm.flask import ScoutApm
import pika, os

app = Flask(__name__)
ScoutApm(app)
app.config["SCOUT_NAME"] = "HMCrawler"
AMQPurl = os.environ.get('CLOUDAMQP_URL', 'amqps://zgumrvzp:***@whale.rmq.cloudamqp.com/zgumrvzp:5672/%2f')
params = pika.URLParameters(AMQPurl)
connection = pika.BlockingConnection(params)
channel = connection.channel()

@app.route("/")
def main():
    """
    Renders the main HTML page.
    :rtype: object
    """
    return render_template('main.html')

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    """
    Renders the output HTML page in case the user submits information.
    :rtype: object
    """
    try:
        search_input = request.form.get("user_input", "")
    except ValueError as err:
        print("An exception occurred:", type(err).__name__)
    populate_db()
    channel.queue_declare(queue='input')
    channel.basic_publish(exchange='',
                          routing_key='input',
                          body=search_input)
    queries = return_store()
    connection.close()
    count_avg = return_count_average(queries)
    price_avg = return_price_average(queries)
    rating_avg = return_rating_average(queries)
    return render_template("output.html", count_avg=count_avg, price_avg=price_avg, rating_avg=rating_avg, queries=queries)

if __name__ == "__main__":
    app.run(debug=True)