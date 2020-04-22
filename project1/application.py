import os
import datetime
from model import *


from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# app.config["SQLALCHEMY_TRACK_MODIFIACTIONS"] = False

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
session = db()

@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/register",methods=["GET", "POST"])
def cont():
    if request.method == "GET":
        return render_template("registration.html")
    else:
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        EmailId = request.form.get("email")
        timestamp = datetime.datetime.now()
        print(username)
        print(EmailId)
        print(timestamp) 
        temp = model(username=username,pwd=pwd,EmailId=EmailId,datetime=timestamp)
        try: 
            session.add(temp)
            print("added")
            session.commit()
            print("commited") 
            return render_template("register.html",username=username)
        except:
            return render_template("errorpage.html")
 
@app.route("/admin")
def table():
    users = db.query(model)
    return render_template("admin.html",user_details=users)

