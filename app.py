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

app = Flask(__name__);
app.config['SECRET_KEY'] = 'my_secret_key'
CORS(app)

@app.route("/")
def index():
    notes = get_notes()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["GET", "POST"])
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

    return render_template("add.html")

@app.route("/view/<int:note_id>")
def view(note_id):
    note = get_note(note_id)
    return render_template("view.html", note=note)

@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
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
    return render_template("edit.html", note=note)


@app.route("/delete/<int:note_id>")
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
        # elif len(cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()) == 1:
        #     flash("Username already taken. Please choose a different username.")

        # Ensure password was submitted
        elif not password or not confirmation:
            flash("Please enter a password and confirm it.")

        # Ensure password and confirmation match
        elif password != confirmation:
            flash("Passwords do not match. Please re-enter the passwords and make sure they match")

        # Insert the new user into the database
        else:
            # cursor.execute("INSERT INTO users(username, hash) values(?, ?)", (username, password))

            # Log the user in and remember him
            # session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", username)[0]["id"]

            # Flash message the user upon successful registration
            flash("Registration successful!")

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")