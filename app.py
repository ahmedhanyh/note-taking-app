import sqlite3
from flask import Flask, render_template, request, redirect, flash
from flask_cors import CORS

connection = sqlite3.connect(":memory:", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    last_mod_date DATETIME DEFAULT CURRENT_TIMESTAMP
)""")
connection.commit()

def add_note(title, content):
    with connection:
        cursor.execute("INSERT INTO notes(title, content) VALUES(:title, :content)",
        {'title': title, 'content': content})

def get_notes():
    cursor.execute("SELECT * FROM notes")
    return cursor.fetchall()

app = Flask(__name__);
app.config['SECRET_KEY'] = 'my_secret_key'
CORS(app)

@app.route("/")
def index():
    notes = get_notes()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["GET", "POST"])
def new():
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

    return render_template("add.html")
