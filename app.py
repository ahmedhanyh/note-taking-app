from helpers import *
from flask import Flask, render_template, request, redirect, flash, session
from flask_session import Session
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__);

# Enable CORS mechanism in application
CORS(app)

# Configure application to use cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.jinja_env.filters["created_since"] = created_since

@app.route("/")
@login_required
def index():
    """Show all user notes"""

    # Retrieve all user notes from database
    notes = get_notes()

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("index.html", username=get_username(), notes=notes)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add a note"""
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        # Ensure title was submitted
        if not title:
            flash("Title must be provided")
        
        # Ensure content was submitted
        elif not content:
            flash("Content must be provided")
        
        # In case title and content were submitted
        else:
            # Add the note to the database
            add_note(title, content)

            # Inform the user that the action succeeded
            flash("Note added successfully!")

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("add.html", username=get_username())

@app.route("/view/<int:note_id>")
@login_required
def view(note_id):
    """View a note"""

    # Retrieve note from database
    note = get_note(note_id)
    
    # Check if user has such note
    if not note:
        # Inform the user that the action succeeded
        flash("Note doesn't exist")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("view.html", username=get_username(), note=note)

@app.route("/edit/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit(note_id):
    """Edit a note"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        # Ensure title was submitted
        if not title:
            flash("Title must be provided")

        # Ensure content was submitted
        elif not content:
            flash("Content must be provided")
        
        # In case title and content were submitted
        else:
            # Update the note in the database
            edit_note(note_id, title, content)

            # Inform the user that the action succeeded
            flash("Note edited successfully!")

            # Redirect user to home page
            return redirect("/")

    # Retrieve note from database
    note = get_note(note_id)

    # Check if user has such note
    if not note:
        # Inform the user that note doesn't exist
        flash("Note doesn't exist")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("edit.html", username=get_username(), note=note)

@app.route("/delete/<int:note_id>")
@login_required
def delete(note_id):
    """Delete a note"""

    # Delete the note from the database
    delete_note(note_id)

    # Inform the user that the action succeeded
    flash("Note deleted successfully!")

    # Redirect user to home page
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
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
            flash("Passwords do not match. Please re-enter the passwords and make sure they match.")

        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO users(username, hash) values(?, ?)", (username, generate_password_hash(password)))

            # Log the user in and remember him
            session["user_id"] = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()[0]

            # Inform the user that the action succeeded
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
        
        else:
            # Query database for username
            rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0][2], password):
                flash("Invalid username and/or password")

            else:
                # Remember which user has logged in
                session["user_id"] = rows[0][0]

                # Inform the user that the action succeeded
                flash("You logged in successfully!")

                # Redirect user to home page
                return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Update user password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        current = request.form.get("current")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure current password was submitted
        if not current:
            flash("Current password must be provided")

        # Ensure new password was submitted
        elif not password or not confirmation:
            flash("Please enter a password and confirm it.")
        
        # In case both current and new password were submitted
        else:
            # Retrieve current password hash value from database
            hash = cursor.execute("SELECT hash FROM users WHERE id = ?", (session["user_id"],)).fetchone()[0]

            # Ensure new password is not the same as current one
            if not check_password_hash(hash, current):
                flash("Current password is not correct. Please make sure to enter it correctly.")
            
            # Ensure password was confirmed correctly
            elif password != confirmation:
                flash("Passwords do not match. Please re-enter the passwords and make sure they match.")
            
            # In case a new password and its confirmation were submitted
            else:
                # Update user password in database
                cursor.execute("UPDATE users SET hash = ? WHERE id = ?", (generate_password_hash(password), session["user_id"]))

                # Inform the user that the action succeeded
                flash("Password updated!")

                # Redirect user to home page
                return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("password.html", username=get_username())

@app.route("/terminate")
def terminate():
    """Delete user account"""

    with connection:
        # Delete user information from database
        cursor.execute("DELETE FROM users WHERE id = ?", (session["user_id"],))

        # Delete all user notes from database
        cursor.execute("DELETE FROM notes WHERE user_id = ?", (session["user_id"],))
    
    # Redirect user to logout page (Log user out)
    return redirect("/logout")
