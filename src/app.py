#!/usr/bin/env python3

import threading, time
from flask import Flask, request, render_template
from src.data_collector import return_store
from src.data_analyzer import return_count_average, return_price_average, return_rating_average
from scout_apm.flask import ScoutApm
from messenger.producer import send_message
from messenger.consumer import consume_message

app = Flask(__name__)
ScoutApm(app)
app.config["SCOUT_NAME"] = "HMCrawler"
thread = threading.Thread(target=consume_message, daemon=True)
thread.start()

@app.route("/")
def main():
    """
    Renders the main HTML page.
    :rtype: object
    """''
    return render_template('main.html')

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    """
    Renders the output HTML page in case the user submits information.
    :rtype: object
    """
    input = ""
    try:
        input = request.form.get("user_input", "")
    except ValueError as err:
        print("An exception occurred:", type(err).__name__)
    send_message(input)
    time.sleep(1)
    queries = return_store(input)
    count_avg = return_count_average(queries)
    price_avg = return_price_average(queries)
    rating_avg = return_rating_average(queries)
    return render_template("output.html", count_avg=count_avg, price_avg=price_avg, rating_avg=rating_avg, queries=queries)

if __name__ == "__main__":
    app.run(debug=True)