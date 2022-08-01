# NotesApp - A Note Taking Web Application
***NotesApp is a small and a simple web application created with bootstrap (frontend) and flask (backend) frameworks. It helps users take notes, edit or delete them.***

I'll write about the project in detail in the next few sections.

## 'templates' directory
**This one contains all the templates (HTML files) that the web application will render.**

I've used the Jinja templating engine (which is the default templating engine that comes integrated with flask) to create the templates. All templates extend the 'layout.html' template. I've used some bootstrap components like a navbar, cards, buttons, a dropdown menu, a modal, and alerts. I've also added some custom styling using css.

## 'static' directory
**It contains stylesheets (CSS files), scripts (JavaScript files), and images.**
### style.css
**This stylesheet contains all the custom styles that were applied to the html pages.**

There are rulesets (blocks of property: value pairs 'aka delcarations') that manage the page's layout using flexbox, replace overflowing text with ellipses, add hover effects on elements, and change elements' background and text colors when in dark mode. To make the input fields' placeholder text color lighter in dark mode, I've used the ```::placeholder``` pseudo-element.

### script.js
**The script is responsible for enabling bootstrap tooltips, being able to hide alerts, highlighting an active navbar item, and switching the dark/light theme.**

#### Dark/Light mode implementation

In 'script.js', we define a property (variable inside an object in JavaScript) on the localStorage object that stores the current theme (either 'light' or 'dark')
```javascript
if (!localStorage.getItem("currentTheme")) {
  localStorage.setItem("currentTheme", "light");
}
```
we first check if 'currentTheme' property is already set, and if it isn't, we set its value to "light".

Next, we create a listener function that gets invoked when the '.switch-theme-btn' button is clicked,
```javascript
function switchTheme() {
  if (localStorage.getItem("currentTheme") === "light") {
    localStorage.setItem("currentTheme", "dark");
  } else {
    localStorage.setItem("currentTheme", "light");
  }

  location.reload();
}

const switchThemeBtn = document.querySelector(".switch-theme-btn");
switchThemeBtn.addEventListener("click", switchTheme);
```
all it does is change the "currentTheme" property's value to either "light" or "dark" depending on its current value, then reloads the page.

Finally, after selecting the DOM elements we'll need to update, we check which theme the user has chosen and apply the styles to these elements accordingly
```javascript
if (localStorage.getItem("currentTheme") === "dark") {
.
.
.
}
```

---

## app.py
**This is the main application file. It contains most of the application's code and functionality.**

The file begins with importing all the modules it'll need.

Then it goes on to create the application and to configure it.

First, it instantiates a Flask application instance of the current file, which is done in line 9 like this:
```python
app = Flask(__name__)
```

Then it allows the application to receive and send cross-origin requests and responses.
```python
CORS(app)
```

It then configures the app to use cookies, which will allow it to remember information even after the web app is closed, like (in our case), the ID of logged in user.
```python
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
```

We add a custom jinja filter 'created_since' which will be used to give us how long ago since a note was created (more on that later).
```python
app.jinja_env.filters["created_since"] = created_since
```

Now, after creating and configuring the application, we create and setup the database that will hold all of the users' data.

In this line of code, we create a connection with 'notesapp.db' database file
```python
connection = sqlite3.connect("notesapp.db", check_same_thread=False)
```
We also create a cursor object to be able to execute SQL queries
```python
cursor = connection.cursor()
```
Here's how we can use this object to create a new table
```python
cursor.execute("""CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            hash TEXT NOT NULL
        )""")
```
The tables' creation code is nested inside a try/except block to avoid raising any exception (specifically, 'table already exists' exception) when re-running the server.

We create two indexes on the 'id' columns in both the 'users' and 'notes' tables to speed up transactions.
```python
cursor.execute("CREATE UNIQUE INDEX 'user_id_index' ON 'users' ('id')")
cursor.execute("CREATE UNIQUE INDEX 'note_id_index' ON 'notes' ('id')")
```

Finally, we close the connection with
```python
connection.close()
```
we'll open it again when we need it (before processing a request).

Next, we create two functions:
1. ```open_db_conn()``` executes before a request is processed (this is done by decorating the function with ```@before_request```). It opens a database connection, creates a cursor object and makes them available globally by adding them to the global ```g``` object provided by flask.
1. ```close_db_conn()``` executes after a request has been processed (this is done by decorating the function with ```@after_request```). It closes the database connection.

The rest of the file contains all the routes' definitions and their view functions. The view functions contain code that makes CRUD operations on the database, server-side validation or just renders a template. Routes that require the user to be logged in are decorated with the ```@login_required``` decorator. This summarizes this part of the file, we won't need to go into detail about each route definition and view function.

---

## helpers.py
**This file contains helper functions.**

It also begins with importing the modules it'll use.

Then we define some functions that abstract code for performing the CRUD operations we'll be doing on the database.
The functions ```get_username()```, ```add_note()```, ```get_notes()```, ```get_note(id)```, ```edit_note(id, title, content)```, ```delete_note(id)``` all perform CRUD operations, and they are always executed during the processing of a request.

Next, we define the ```login_required(f)``` function that'll be used to decorate routes that require a user to be logged in. More can be found in the [documentation](https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/).

Finally, we define the ```created_since(note_id)``` function that takes a note's ID and returns how long ago since that note was created in the form of a string formatted like: '[amount of time] [days|months|years] ago'. The format differs based on the amount of time, for example, 'less than a day' is returned in case the amount of time is less than a day.

---

## requirements.txt
**Contains the names and versions of the packages used in the project.**
