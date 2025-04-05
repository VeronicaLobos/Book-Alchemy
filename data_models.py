from sqlalchemy import Integer, String, ForeignKey
from flask_sqlalchemy import SQLAlchemy

# Flask-SQLAlchemy instance
db = SQLAlchemy()

class Author(db.Model):
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
    __tablename__ = 'books'
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(Integer)
    title = db.Column(String)
    publication_date = db.Column(String)
    author_id = db.Column(Integer, ForeignKey('authors.id'))
    author = db.relationship("Author", back_populates="books")

    def __repr__(self):
        return (f"Book(id={self.id}, isbn={self.isbn}, "
                f"title='{self.title}', "
                f"publication_date='{self.publication_date}', "
                f"author_id={self.author_id})")
