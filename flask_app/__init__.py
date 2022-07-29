# __init__.py
from flask import Flask, render_template, redirect, request, session, flash
# from flask_googlemaps import GoogleMaps

app = Flask(__name__)
app.secret_key = "hey"




# you can also pass the key here if you prefer
# GoogleMaps(app, key="8JZ7i18MjFuM35dJHq70n3Hx4")