from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

# Create a Flask app instance
app = Flask(__name__)
# Create a SQLAlchemy instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
# Connect the Flask app to the flask-sqlalchemy code
db.init_app(app)

