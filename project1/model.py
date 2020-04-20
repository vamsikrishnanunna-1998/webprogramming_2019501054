from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class model(db.Model):
    __tablename__ = "Usersdb"
    # id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable=False, primary_key=True)
    pwd = db.Column(db.String,nullable=False)
    EmailId = db.Column(db.String, nullable=False)
    datetime = db.Column(db.String,nullable=False)

'''
Class for storing book details
'''
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(80), index=False, unique=True, nullable=False)
    title = db.Column(db.String(80), index=True, unique=False, nullable=False)
    author = db.Column(db.String(128))
    year = db.Column(db.Integer, index=False, unique=False, nullable=False)

    def __init__(self, isbn, title, author, year) :
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self):
        return self.title
