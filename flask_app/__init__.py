"""
This is main module that should be ran on
the server
"""

from flask import Flask
from flask_app.my_config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# create main app
app = Flask(__name__)
# config for security in forms and other things
app.config.from_object(Config)

# connect data base
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# connect login manager
login = LoginManager(app)
login.login_view = "login"

from flask_app import routes, models

db.create_all()
app.run(debug=True)
