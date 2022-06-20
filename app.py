import sqlite3
from flask import Flask, render_template, request, redirect, flash, session
from flask_session import Session
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__);
CORS(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

connection = sqlite3.connect(":memory:", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL
)""")
connection.commit()

cursor.execute("""CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    last_mod_date DATETIME DEFAULT CURRENT_TIMESTAMP
)""")
connection.commit()

def get_username():
    """Get username of logged in user"""

    # Query database for username of logged in user
    cursor.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))

    # Return the username
    return cursor.fetchone()[0]

def add_note(title, content):
    with connection:
        cursor.execute("INSERT INTO notes(title, content) VALUES(:title, :content)",
        { 'title': title, 'content': content })

def get_notes():
    cursor.execute("SELECT * FROM notes")
    return cursor.fetchall()

def get_note(id):
    cursor.execute("SELECT * FROM notes WHERE id = ?", (id,))
    return cursor.fetchone()

def edit_note(id, title, content):
    with connection:
        cursor.execute("UPDATE notes SET title = :title, content = :content WHERE id = :id",
        { 'title': title, 'content': content, 'id': id })

def delete_note(id):
    with connection:
        cursor.execute("DELETE FROM notes WHERE id = ?", (id,))

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    notes = get_notes()
    return render_template("index.html", username=get_username(), notes=notes)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title:
            flash("Title must be provided")
        elif not content:
            flash("Content must be provided")
        else:
            add_note(title, content)
            flash("Note added successfully!")
            return redirect("/")

    return render_template("add.html", username=get_username())

@app.route("/view/<int:note_id>")
@login_required
def view(note_id):
    note = get_note(note_id)
    return render_template("view.html", username=get_username(), note=note)

@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit(note_id):
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title:
            flash("Title must be provided")
        elif not content:
            flash("Content must be provided")
        else:
            edit_note(note_id, title, content)
            flash("Note edited successfully!")
            return redirect("/")

    note = get_note(note_id)
    return render_template("edit.html", username=get_username(), note=note)

@app.route("/delete/<int:note_id>")
@login_required
def delete(note_id):
    delete_note(note_id)
    flash("Note deleted successfully!")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Extract the username, password and its confirmation
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            flash("Please choose a username")

        # Ensure username does not already exist
        elif len(cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()) == 1:
            flash("Username already taken. Please choose a different username.")

        # Ensure password was submitted
        elif not password or not confirmation:
            flash("Please enter a password and confirm it.")

        # Ensure password and confirmation match
        elif password != confirmation:
            flash("Passwords do not match. Please re-enter the passwords and make sure they match")

        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO users(username, hash) values(?, ?)", (username, generate_password_hash(password)))

            # Log the user in and remember him
            session["user_id"] = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()[0]

            # Flash message the user upon successful registration
            flash("Registration successful!")

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flash("Username must be provided")

        # Ensure password was submitted
        elif not password:
            flash("Password must be provided")

        # Query database for username
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], password):
            flash("Invalid username and/or password")

        else:
            # Remember which user has logged in
            session["user_id"] = rows[0][0]

            # Flash message the user if logged in successfully
            flash("You logged in successfully!")

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
