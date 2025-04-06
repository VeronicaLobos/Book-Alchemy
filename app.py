"""
This is a simple Flask application that uses SQLAlchemy to
manage a library database.
This module sets up the Flask application and SQLAlchemy
database connection.

It defines several API endpoints to interact with the
library database, including:
- Retrieving all books
- Adding a new author
- Adding a new book
- Deleting a book
The application uses SQLite as the database backend and
Jinja2 templates for rendering HTML pages.
The application is designed to be run locally and opens
a web browser to display the home page when started.
"""

from flask import Flask, request, render_template
from sqlalchemy import asc, desc
import os
import webbrowser
from data_models import db, Author, Book

app = Flask(__name__, static_folder='_static')
database_path = os.path.join(os.path.dirname(__file__),
                             'data','library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
db.init_app(app)

## Create the database and tables, if they don't exist
with app.app_context():
    db.create_all()


#### API endpoints ####

@app.route('/home')
def get_books():
    """
    Returns a list of all books in the database.

    Queries the database for all books and their authors,
    sorts the results based on the sort_by and order parameters,
    and returns a list of dictionaries containing the book data.
    Each dictionary contains the book's ID, ISBN, title,
    publication date, and author ID.
    It returns a render of the home.html template with the
    list of books.
    """
    ## Get the sort_by and order parameters from the request
    search_term = request.args.get('search', '')
    sort_by = request.args.get('sort', 'title')
    order = request.args.get('order', 'asc')

    ## Query the database for all books and their authors
    ## and sort the results based on the sort_by and order parameters
    query = Book.query.join(Author)

    if search_term:
        query = query.filter(Book.title.ilike(f'%{search_term}%') |
                           Author.name.ilike(f'%{search_term}%'))
        if not query.all():
            ## If no books are found, show an error message
            message = f"Search term '{search_term}' not found."
            return render_template('home.html', message=message)

    if sort_by == 'title':
        query = query.order_by(asc(Book.title)
                               if order == 'asc' else desc(Book.title))
    elif sort_by == 'author':
        query = query.order_by(asc(Author.name)
                               if order == 'asc' else desc(Author.name))
    elif sort_by == 'year':
        query = query.order_by(asc(Book.year)
                               if order == 'asc' else desc(Book.year))

    all_books = query.all()

    ## Create a list of dictionaries containing the book data
    books_data = []
    for book in all_books:
        book_data = {
            'id': book.id,
            'isbn': book.isbn,
            'title': book.title,
            'year': book.year,
            'author': book.author.name,
            'cover': book.cover,
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
    form, checks if the author already exists in the database:
     - If the author already exists, it returns an error message.
        - If the author does not exist, it adds the new author
        to the database and returns a success message.
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
    """
    Adds a new book to the database.

    If a Get request is made, it returns a render of the
    add_book.html template.

    If a Post request is made, it retrieves the data from the
    form, checks if the book already exists in the database:
        - If the book already exists, it returns an error message.
        - If the book does not exist:
            - It retrieves the author ID from the database.
            - It creates a new book object and adds it to the
            database.
            - It returns a success message.
    """
    if request.method == 'POST':
        ## Get the data from the form
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year')

        ## Retrieve the author ID from the database
        author_obj = Author.query.filter_by(name=author).first()
        if author_obj:
            author_id = author_obj.id
        else:
            ## If the author does not exist, show an error message
            message = (f"{author} not found in the database."
                       f"Please add the author first.")
            return render_template('add_book.html', message=message)

        ## Get the book cover image URL from Open Library API
        if isbn:
            cover = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
        else:
            cover = "https://covers.openlibrary.org/b/isbn/142157537X-M.jpg"

        ## Create a new book object
        new_book = Book(
                isbn=isbn,
                title=title,
                year=year,
                author_id=author_id,
                cover=cover
        )

        ## Check if the book already exists in the database
        existing_book = Book.query.filter_by(isbn=new_book.isbn).first()
        if existing_book:
            ## If the book already exists, show an error message
            message = f"Book with ISBN '{new_book.isbn}' already exists."
            return render_template('add_book.html', message=message)

        ## Add the new book to the database
        db.session.add(new_book)
        db.session.commit()

        ## Show a success message
        message = f"Book '{new_book.title}' added successfully."
        return render_template('add_book.html', message=message)

    return render_template('add_book.html')


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Deletes a book from the database (sad).

    If a Post request is made through the delete button in the
    home.html template, it retrieves the book ID from the
    URL.

    If the book exists, it deletes the book from the database
    and returns a success message.
    If the book does not exist, it returns an error message.

    Checks if the author has any other books in the database.
    If the author has no other books, it deletes the author...
    ... but I prefer not to delete the author.
    """
    book = Book.query.get(book_id)
    if book:
        #author_id = book.author_id
        db.session.delete(book)
        db.session.commit()

        ## Check if the author has any other books in the database
        #author = Author.query.get(author_id)
        #if not author.books:
        #    db.session.delete(author)
        #    db.session.commit()

        message = f"Book '{book.title}' deleted successfully."
    else:
        message = "Book not found."

    return render_template('home.html', message=message)


if __name__ == '__main__':
    url = 'http://127.0.0.1:5002/home'
    webbrowser.open_new(url)
    app.run(port=5002, debug=True)
