
import requests
import sqlite3


def weather(params=None):
    if params is None:
        params = values

    URL = "http://api.openweathermap.org/data/2.5/weather"
    response = requests.get(URL, params=params)

    json = response.json()

    soln = []
    for value in json:
        if value == "weather":
            soln.append(json[value][0]["description"])

        if value == "main":
            soln.append(json[value]["temp"])

        if value == "sys":
            soln.append(json[value]["country"])

        if value == "name":
            soln.append(json[value])

        if value == "timezone":
            soln.append(json[value])

    return soln


def time_zone_change(time_in_sec):

    hrs, dot, m = str(time_in_sec/3600).partition(".")
    m = str(int((float(dot + m))*60))
    if time_in_sec < 0:
        return "GMT " + hrs + ":" + m
    return "GMT +" + hrs + ":" + m


def finished(value):
    final = []
    db = sqlite3.connect("codes.db")
    db.row_factory = sqlite3.Row
    try:
        a, b, c, d, e = weather(value)
    except ValueError:
        return None

    final.append(e)
    final.append(a)
    final.append((str(b) + '°C'))
    value = db.execute("SELECT country FROM country_code WHERE Alpha2 = (?)", (c,)).fetchall()

    final.append(value[0]['country'] + ' (' + time_zone_change(d) + ')')

    return final
