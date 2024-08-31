#!/usr/bin/env python3

from flask import Flask, request, requests, render_template
'from Databases.Weather import Weather, db'

app = Flask(__name__)
URL = 'https://fakestoreapi.com/products'

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    response = requests.get(URL)
    print(response.content)
    return "You entered: " + input_text