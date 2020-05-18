import os

import requests

# Import table definitions.
from models import *

from flask import Flask, session, render_template, redirect, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__, static_url_path='', static_folder='static')

# Sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Tell Flask what SQLAlchemy database to use.
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database
db.init_app(app)

@app.route("/")
def index():
    #res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "ihn5YquU1DXQgEd9MotEA", "isbns": "9781632168146"})
    #print(res.json())
    if session.get("user_id") is None:
        return redirect("/login")

    user = User.query.get(session.get("user_id"))

    return render_template("index.html", userName=user.name)

@app.route("/search", methods=["POST"])
def search():
    if session.get("user_id") is None:
        return redirect("/login")

    isbn = request.form.get("isbn") 
    # 1. read what was sent us (isbn, title or author)
    # 2. query the DB and get results
    # 3. return a search_results.html file which should be passed to the template engine together with the fetched data
    return render_template("search_results.html", isbn=isbn)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/do_login", methods=["POST"])
def do_login():
    # In terms of how to “log a user in,” recall that you can store information inside of the session, which can store different values for different users. In particular, if each user has an id, then you could store that id in the session (e.g., in session["user_id"]) to keep track of which user is currently logged in.

    # 1. read data sent from client: username and password
    username = request.form.get("username")
    password = request.form.get("password")
    # 2. query database for a User with that username
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template("login.html", message="Whoops, user not found. Please, try again.")
    # 3. compare passwords
    if user.password != password:
        return render_template("login.html", message="Whoops, password not correct. Please, try again.")
    # 4. store the user id in the session scope
    session["user_id"] = user.id
    # 5. return to index.html
    return redirect("/")

@app.route("/do_logout", methods=["POST"])
def do_logout():
    session.clear()
    return redirect("/login")

# show registration form 
@app.route("/registration")
def registration():
    return render_template("registration.html")

# create a new user 
@app.route("/register_user", methods=["POST"])
def register_user():
    # 1. read data sent from client: username and password
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    # 2. validate the data

    # 3. create a new User object
    user = User(name=name, username=username, password=password)

    # 4. store that User object in the DB
    db.session.add(user)
    db.session.flush()
    db.session.commit()

    # 5. Log the user in automatically by storing the user id in the session scope
    session["user_id"] = user.id

    # 6. return some html file to client
    return redirect("/")

# test: list all users
@app.route("/list_users")
def list_users():
    users = User.query.all()

    usernames = []
    for user in users:
        usernames.append(user.username)

    return jsonify({
        "users": usernames
    })