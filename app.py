from flask import Flask, render_template, redirect, request
from api import finished
import os

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if request.form.get('city'):
            value = {
                "q": f"{request.form.get('city')}",
                "appid": os.environ['OPEN_WEATHER_API_KEY'],
                "units": "metric"
            }
            THE_WEATHER = finished(value)

            return render_template("index.html", the_weather=THE_WEATHER)

    return render_template("index.html")
