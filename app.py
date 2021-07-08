
from sqlite3.dbapi2 import threadsafety
from flask import Flask, render_template, redirect, request, jsonify, session
from flask.helpers import url_for
from api import finished
import os

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        if request.form.get('city'):
            value = {
                "q": f"{request.form.get('city')}",
                "appid": os.environ.get('OPEN_WEATHER_API_KEY'),
                "units": "metric"
            }
            if finished(value) is None:
                return redirect(url_for("index"))

            return render_template("index.html", the_weather=finished(value))

    return render_template("index.html")
