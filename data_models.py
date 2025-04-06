"""
This module defines the data models for the application
using SQLAlchemy.

* db is an instance of SQLAlchemy that is used to interact
with the database.

* Author and Book classes, which represent authors and books
tables in the database, respectively.
"""

from sqlalchemy import Integer, String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import requests as req

# Flask-SQLAlchemy instance
db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author in the database.
    Attributes:
        id (int): The unique identifier for the author.
        name (str): The name of the author.
        birth_date (str): The birthdate of the author.
        date_of_death (str): The date of death of the author.
        books (list): A list of books written by the author.
    Methods:
        __repr__(): Returns a string representation of the author.
    """
    __tablename__ = 'authors'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String)
    birth_date = db.Column(String)
    date_of_death = db.Column(String)
    books = db.relationship("Book", back_populates="author")

    def __repr__(self):
        return (f"Author(id={self.id}, name='{self.name}', "
                f"birth_date='{self.birth_date}', "
                f"date_of_death='{self.date_of_death}')")


class Book(db.Model):
    """
    Represents a book in the database.
    Attributes:
        id (int): The unique identifier for the book.
        isbn (int): The ISBN-number of the book.
        title (str): The title of the book.
        publication_date (str): The publication year of the book.
        author_id (int): The ID of the author of the book.
        author (Author): The author of the book.
    """
    __tablename__ = 'books'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(Integer)
    title = db.Column(String)
    year = db.Column(Integer)
    cover = db.Column(String)
    author_id = db.Column(Integer, ForeignKey('authors.id'))
    author = db.relationship("Author", back_populates="books")

    def __repr__(self):
        return (f"Book(id={self.id}, isbn={self.isbn}, "
                f"title='{self.title}', "
                f"publication_date='{self.publication_date}', "
                f"author_id={self.author_id})")
