
from flask.globals import current_app
import requests
import psycopg2

def weather(params=None):
    if params is None:
        return

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

    try:
        a, b, c, d, e = weather(value)
    except ValueError:
        return None
    
    conn = psycopg2.connect(current_app.config['DATABASE'])
    db = conn.cursor()
        
    final.append(e)
    final.append(a)
    final.append((str(b) + '°C'))
    
    db.execute("SELECT country FROM country_code WHERE Alpha2 = %s",(c,))
    value = db.fetchone()
    
    final.append(value[0]+ ' (' + time_zone_change(d) + ')')

    db.close()
    conn.close()

    return final
