# Book Alchemy

![download](https://github.com/user-attachments/assets/2017340a-ade3-47f6-8fef-2c8a0696386e)

This is a graded project from the bootcamp I attended, and it is
intended to practice the use of Flask and SQLAlchemy.
The application is designed to be run locally and opens
a web browser to display the home page when started.

It defines several API endpoints to interact with the library database:
- Retrieving all books
- Adding a new author
- Adding a new book
- Deleting a book

## Technologies Used
- _Python 3.12........_ for the data classes and the main application logic
- _Flask..................._ for creating the web application
- _SQLAlchemy......._ for ORM (Object Relational Mapping)
- _SQLite................._ for a lightweight database
- _Jinja2..................._ for rendering HTML templates
- _HTML/CSS.........._ for the front-end, including a simple intuitive responsive design
- _JavaScript..........._ redirecting to the home page, and displaying alerts for wrong inputs

## Project structure
```text
book-alchemy/
├── app.py
├── /_static
│   └── style.css
├── /templates
│   ├── add_book.html
│   ├── add_author.html
│   ├── delete_book.html
│   ├── home.html
│   └── redirect.html
├── /data
│   └── library.sqlite
├── app.py
├── data_models.py
├── requirements.txt
└── README.md
```