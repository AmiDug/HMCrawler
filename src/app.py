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
    query = return_store(search_input)
    print(return_count_average(query))
    print(return_price_average(query))
    print(return_rating_average(query))
    return query

if __name__ == "__main__":
    app.run() #delete later