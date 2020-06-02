# from docx import Document
from flask import Flask, render_template, request, redirect, url_for, session
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

from flack_app.my_config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from flack_app import routes, models

if __name__ == '__main__':
    app.run(debug=True)
