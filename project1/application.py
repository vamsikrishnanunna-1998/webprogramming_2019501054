import os
import datetime
from model import *


from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

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
SESSION = db()

@app.route("/")
def index():
    if session.get("username") is not None:
        return render_template("login.html", username= session.get("username"))
    return redirect("/register")
 
@app.route("/register",methods=["GET", "POST"])
def form():
    if session.get("username") != None:
        return render_template("login.html", username= session.get("username"))
    if request.method == "GET":
        return render_template("registration.html",data = "Please Login")
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
            SESSION.add(temp)
            print("added")
            SESSION.commit()
            print("commited") 
            return render_template("registration.html", data="Registered successfully, Please Login")
        except:
            return render_template("registration.html",text="User already exists, Please Login")
 
@app.route("/admin", methods = ["GET"])
def table():
    users = db.query(model)
    return render_template("admin.html",user_details=users)

@app.route("/auth", methods = ["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        email = request.form.get("email")
        user = db.query(model).get(username)
        session["username"] = username
        if user != None:
            if pwd == user.pwd:
                return render_template("login.html",username=username)
            else:
                return render_template("registration.html",username="please enter correct password")
        else:
            return render_template("registration.html",username="Entered Wrong username, please try again")
                    
@app.route("/logout",methods = ["GET"])
def logout():
    session.clear()
    return redirect("/register")
    

