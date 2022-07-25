# imports
from flask_app import app, render_template, redirect, request, session, flash
import pprint
pp = pprint.PrettyPrinter(indent=4)


@app.errorhandler(404) 
def invalid_route(e): 
    return render_template('error_404.html')