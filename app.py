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
    add_author.html template with a form to add a new author.

    If a Post request is made, it retrieves the data from the
    form, checks if the author name is empty, and
    checks if the author already exists in the database:
    - If the author name is empty, it returns an error message.
    - If the author already exists, it returns an error message.
    - If the author does not exist, it adds the new author
      to the database and returns a success message.
    """
    if request.method == 'POST':
        author_name = request.form.get('name')
        name = author_name.strip()
        if not name:
            message = "Author name cannot be empty."
            return render_template('add_author.html',
                                   message=message)

        new_author = Author(
            name=name,
            birth_date=request.form.get('birth_date'),
            date_of_death=request.form.get('date_of_death')
        )

        existing_author = Author.query.filter_by(name=new_author.name).first()
        if existing_author:
            message = f"Author '{new_author.name}' already exists."
            return render_template('add_author.html',
                                   message=message)

        db.session.add(new_author)
        db.session.commit()

        message = f"Author '{new_author.name}' added successfully."
        return render_template('add_author.html',
                               message=message)

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Adds a new book to the database.

    It retrieves all authors from the database and
    passes them to the template (for the author down-drop
    menu). It passes it after an error or after adding a book,
    so the user can keep trying to add a book.

    If a Get request is made, it returns a render of the
    add_book.html template with a form to add a new book.

    If a Post request is made, it retrieves the data from
    the form:
    - retrieves the author ID from the database
    - checks if the book already exists in the database by
      checking the ISBN, if it does, it returns an error
      message
    """
    authors = Author.query.all()
    authors = [author.name for author in authors]

    if request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year')


        existing_book = Book.query.filter_by(isbn=isbn).first()
        if existing_book:
            message = (f"Book with ISBN '{isbn}', '{existing_book.title}',"
                       f" already exists.")
            return render_template('add_book.html',
                                   message=message,
                                   authors=authors)

        if isbn:
            cover = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
        else:
            cover = "https://covers.openlibrary.org/b/isbn/142157537X-M.jpg"

        author_obj = Author.query.filter_by(name=author).first()
        author_id = author_obj.id
        new_book = Book(
                isbn=isbn,
                title=title,
                year=year,
                author_id=author_id,
                cover=cover
        )

        db.session.add(new_book)
        db.session.commit()

        message = f"Book '{new_book.title}' added successfully."
        return render_template('add_book.html',
                               message=message,
                               authors=authors)

    return render_template('add_book.html',
                           authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['GET', 'POST'])
def delete_book(book_id):
    """
    Deletes a book from the database (sad).

    If a Get request is made, it returns a render of the
    delete_book.html template with the book ID.
    Asks the user to confirm the deletion of the book.
    If the user cancels the deletion, it redirects to the home page.

    If a Post request is made, it retrieves the book ID and the
    author ID from the database.
    If the book does not exist, it returns an error message.
    If the book exists, it deletes the book from the database.
    If the author has no other books, it deletes the author
    from the database.
    After deletion, it returns a success message and redirects
    to the home page.
    """
    if request.method == 'POST':
        book = Book.query.get(book_id)
        author = book.author if book else None
        if book:
            db.session.delete(book)
            db.session.commit()

            if not author.books:
               db.session.delete(author)
               db.session.commit()

            status = "Success!"
            message = f"Book '{book.title}' deleted successfully."
        else:
            status = "Error!"
            message = "Book not found."

        return render_template('redirect.html',
                               message=message,
                               status=status)

    return render_template('delete_book.html',
                           book_id=book_id)


if __name__ == '__main__':
    url = 'http://127.0.0.1:5002/home'
    webbrowser.open_new(url)
    app.run(port=5002, debug=True)
