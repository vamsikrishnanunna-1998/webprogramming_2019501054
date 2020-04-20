"""
importing data from books.csv to postgresql
"""
import os, csv
from flask import Flask, render_template, request
from model import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
"""
main method to create table and insert data.
"""
def main():
	#to create the table.
    db.create_all()
    #reading the file and insertion data into database.
    with open("books.csv", 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            newBook = Book(row[0], row[1], row[2], int(row[3]))
            db.session.add(newBook)
    db.session.commit()

if __name__ == "__main__":
  with app.app_context():
      main()
