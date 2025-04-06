"""
This is a simple Flask application that uses SQLAlchemy to
manage a library database.
This module sets up the Flask application and SQLAlchemy
database connection.
"""

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
import webbrowser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:////Users/veronica/PycharmProjects/Book-Alchemy/data/library.sqlite'
db.init_app(app)

## Create the database and tables
#with app.app_context():
#    db.create_all()


## API endpoints

@app.route('/')
def get_books():
    """
    Returns a list of all books in the database.

    Queries the database for all books and returns a list of
    dictionaries containing the book data. Each dictionary
    contains the book's ID, ISBN, title, publication date,
    and author ID. The list of dictionaries is then rendered
    in the 'home.html' template.
    """
    all_books = Book.query.all()

    books_data = []
    for book in all_books:
        book_data = {
            'id': book.id,
            'isbn': book.isbn,
            'title': book.title,
            'publication_date': book.publication_date,
            'author': book.author.name,
        }
        books_data.append(book_data)

    return render_template('home.html', books=books_data), 200


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Adds a new author to the database.

    If a Get request is made, it returns a render of the
    add_author.html template.

    If a Post request is made, it retrieves the data from the
    form, checks if the author already exists in the database,
    and if not, adds the new author to the database.
    If the author already exists, it returns an error message.
    """
    if request.method == 'POST':
        ## Get the data from the form
        new_author = Author(
            name=request.form.get('name'),
            birth_date=request.form.get('birth_date'),
            date_of_death=request.form.get('date_of_death')
        )

        ## Check if the author already exists in the database
        existing_author = Author.query.filter_by(name=new_author.name).first()
        if existing_author:
            ## If the author already exists, show an error message
            message = f"Author '{new_author.name}' already exists."
            return render_template('add_author.html', message=message)

        ## Add the new author to the database
        db.session.add(new_author)
        db.session.commit()

        ## Show a success message
        message = f"Author '{new_author.name}' added successfully."
        return render_template('add_author.html', message=message)

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    pass


if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5000/add_author')
    app.run(debug=True)
