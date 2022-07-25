from flask_app import app
from flask_app.controllers import users, events, error_handlers

if __name__ == "__main__":
    app.run(debug=True)