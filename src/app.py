#!/usr/bin/env python3

from flask import Flask, request, render_template
from DataCollector import return_store, populate_db
from DataAnalyzer import return_count_average, return_price_average, return_rating_average

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    search_input = request.form.get("user_input", "")
    populate_db()
    queries = return_store(search_input)
    count_avg = return_count_average(queries)
    price_avg = return_price_average(queries)
    rating_avg = return_rating_average(queries)
    return render_template("output.html", count_avg=count_avg, price_avg=price_avg, rating_avg=rating_avg, queries=queries)

if __name__ == "__main__":
    app.run() #delete later