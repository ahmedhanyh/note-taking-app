import datetime
import sqlite3
from flask import render_template, request, redirect, session
from functools import wraps
import math

# Connect to the database "notesapp.db"
connection = sqlite3.connect("notesapp.db", check_same_thread=False)

# Create a cursor instance which allows us to execute SQL queries on "notesapp.db"
cursor = connection.cursor()

# Silence any error that may arise when creating tables
# (in this case creating a table that already exists will throw an error)
try:
    with connection:
        cursor.execute("""CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            hash TEXT NOT NULL
        )""")

        cursor.execute("""CREATE TABLE notes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            content TEXT,
            creation_date DATETIME,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")
except:
    pass

def get_username():
    """Get username of logged in user"""

    cursor.execute("SELECT username FROM users WHERE id = ?",
                    (session["user_id"],))
    return cursor.fetchone()[0]

def add_note(title, content):
    """Add note to database"""

    with connection:
        # Get timestamp for current time
        timestamp_obj = datetime.datetime.now()
        timestamp = timestamp_obj.strftime("%I:%S %p - %b %d, %Y")

        cursor.execute("INSERT INTO notes(user_id, title, content, creation_date) VALUES(?, ?, ?, ?)",
                        (session["user_id"], title, content, timestamp))

def get_notes():
    """Retrieve all notes from database"""

    cursor.execute("SELECT * FROM notes WHERE user_id = ?",
                    (session["user_id"],))
    return cursor.fetchall()

def get_note(id):
    """Retrieve a note from database by its id"""

    cursor.execute("SELECT * FROM notes WHERE id = ? and user_id = ?",
                    (id, session["user_id"]))
    return cursor.fetchone()

def edit_note(id, title, content):
    """Edit note and update database"""

    with connection:
        cursor.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?",
                        (title, content, id))

def delete_note(id):
    """Delete a note from database"""

    # Connect to the database
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

def created_since(note_id):
    cursor.execute("SELECT creation_date FROM notes WHERE id = ?", (note_id,))
    creation_date = datetime.datetime.strptime(cursor.fetchone()[0], "%I:%S %p - %b %d, %Y")
    time_since = datetime.datetime.now() - creation_date

    time_since_in_years = math.floor(time_since.days / 365)
    if time_since_in_years:
        if time_since_in_years == 1:
            return "a year ago"
        return f"{time_since_in_years} years ago"
    
    time_since_in_months = math.floor(time_since.days / 30)
    if time_since_in_months:
        if time_since_in_months == 1:
            return "a month ago"
        return f"{time_since_in_months} months ago"
    
    if time_since.days:
        if time_since.days == 1:
            return "a day ago"
        return f"{time_since.days} days ago"

    return "less than a day ago"