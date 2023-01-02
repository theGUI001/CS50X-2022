---
files: [app.py]
url: https://cdn.cs50.net/2022/fall/labs/9/birthdays/README.md
window: [terminal]
---

# Lab 9: Birthdays

{% alert warning %}

Labs are practice problems which, time permitting, may be started or completed in your {% if college %}lab{% else %}section{% endif %}, and are assessed on correctness only. You are encouraged to collaborate with classmates on this lab, though each member in a group collaborating is expected to contribute equally to the lab.

{% endalert %}

Create a web application to keep track of friends' birthdays.

![screenshot of birthdays website](birthdays.png)

## Understanding

In `app.py`, you'll find the start of a Flask web application. The application has one route (`/`) that accepts both `POST` requests (after the `if`) and `GET` requests (after the `else`). Currently, when the `/` route is requested via `GET`, the `index.html` template is rendered. When the `/` route is requested via `POST`, the user is redirected back to `/` via `GET`.

`birthdays.db` is a SQLite database with one table, `birthdays`, that has four columns: `id`, `name`, `month`, and `day`. There are a few rows already in this table, though ultimately your web application will support the ability to insert rows into this table!

In the `static` directory is a `styles.css` file containing the CSS code for this web application. No need to edit this file, though you're welcome to if you'd like!

In the `templates` directory is an `index.html` file that will be rendered when the user views your web application.

## Implementation Details

Complete the implementation of a web application to let users store and keep track of birthdays.

* When the `/` route is requested via `GET`, your web application should display, in a table, all of the people in your database along with their birthdays.
    * First, in `app.py`, add logic in your `GET` request handling to query the `birthdays.db` database for all birthdays. Pass all of that data to your `index.html` template.
    * Then, in `index.html`, add logic to render each birthday as a row in the table. Each row should have two columns: one column for the person's name and another column for the person's birthday.
* When the `/` route is requested via `POST`, your web application should add a new birthday to your database and then re-render the index page.
    * First, in `index.html`, add an HTML form. The form should let users type in a name, a birthday month, and a birthday day. Be sure the form submits to `/` (its "action") with a method of `post`.
    * Then, in `app.py`, add logic in your `POST` request handling to `INSERT` a new row into the `birthdays` table based on the data supplied by the user.

Optionally, you may also:

* Add the ability to delete and/or edit birthday entries.
* Add any additional features of your choosing!

### Walkthrough

{% alert primary %}

This video was recorded when the course was still using CS50 IDE for writing code. Though the interface may look different from your codespace, the behavior of the two environments should be largely similar!

{% endalert %}

{% video https://video.cs50.io/HXwvj8x1Fcs %}

### Hints

* Recall that you can call `db.execute` to execute SQL queries within `app.py`.
    * If you call `db.execute` to run a `SELECT` query, recall that the function will return to you a list of dictionaries, where each dictionary represents one row returned by your query.
* You'll likely find it helpful to pass in additional data to `render_template()` in your `index` function so that access birthday data inside of your `index.html` template.
* Recall that the `tr` tag can be used to create a table row and the `td` tag can be used to create a table data cell.
* Recall that, with Jinja, you can create a [`for` loop](https://jinja.palletsprojects.com/en/2.11.x/templates/#for) inside your `index.html` file.
* In `app.py`, you can obtain the data `POST`ed by the user's form submission via `request.form.get(field)` where `field` is a string representing the `name` attribute of an `input` from your form.
  * For example, if in `index.html`, you had an `<input name="foo" type="text">`, you could use `request.form.get("foo")` in `app.py` to extract the user's input.

{% spoiler "Not sure how to solve?" %}

{% video https://video.cs50.io/lVwv4o8vmvI %}

{% endspoiler %}

### Testing

No `check50` for this lab! But be sure to test your web application by adding some birthdays and ensuring that the data appears in your table as expected.

Run `flask run` in your terminal while in your `birthdays` directory to start a web server that serves your Flask application.

## How to Submit

1. While in your birthdays directory, create a ZIP file of your Flask application by executing:

```
zip -r birthdays.zip *
```

{:start="2"}
1. Download your `birthdays.zip` file by control-clicking or right-clicking on the file in your codespace's file browser and choosing **Download**.
2. Go to CS50's [Gradescope page](https://www.gradescope.com/courses/).
3. Click "Lab 9: Birthdays".
4. Drag and drop your `birthdays.zip` file to the area that says "Drag & Drop". Be sure it has that **exact** filename! If you upload a file with a different name, the autograder likely will fail when trying to run it, and ensuring you have uploaded files with the correct filename is your responsibility!
5. Click "Upload".

You should see a message that says "Lab 9: Birthdays" submitted successfully!"

{% alert danger %}

Per Step 4 above, after you submit, be sure to check your autograder results. If you see `SUBMISSION ERROR: missing files (0.0/1.0)`, it means your file was not named exactly as prescribed (or you uploaded it to the wrong problem).

Correctness in submissions entails everything from reading the specification, writing code that is compliant with it, and submitting files with the correct name. If you see this error, you should resubmit right away, making sure your submission is fully compliant with the specification. The staff will not adjust your filenames for you after the fact!

{% endalert %}

Want to see the staff's solution?
{% spoiler "app.py" %}
```python
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Access form data
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Insert data into database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        # Go back to homepage
        return redirect("/")

    else:

        # Query for all birthdays
        birthdays = db.execute("SELECT * FROM birthdays")

        # Render birthdays page
        return render_template("index.html", birthdays=birthdays)
```
{% endspoiler %}

{% spoiler "index.html" %}
```html
<!DOCTYPE html>

<html lang="en">
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500&display=swap" rel="stylesheet">
        <link href="/static/styles.css" rel="stylesheet">
        <title>Birthdays</title>
    </head>
    <body>
        <div class="jumbotron">
            <h1>Birthdays</h1>
        </div>
        <div class="container">
            <div class="section">

                <h2>Add a birthday.</h2>
                <form action="/" method="POST">
                    <input name="name" placeholder="Name" type="text">
                    <input name="month" placeholder="Month" type="number" min="1" max="12">
                    <input name="day" placeholder="Day" type="number" min="1" max="31">
                    <input type="submit" value="Add Birthday">
                </form>
            </div>

            <div class="section">
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Birthday</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% raw %}{% for birthday in birthdays %}
                            <tr>
                                <td>{{ birthday.name }}</td>
                                <td>{{ birthday.month }}/{{ birthday.day }}</td>
                            </tr>
                        {% endfor %}{% endraw %}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
</html>
```
{% endspoiler %}

{% spoiler "styles.css" %}
```css
body {
    background-color: #fff;
    color: #212529;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    margin: 0;
    text-align: left;
}

.container {
    margin-left: auto;
    margin-right: auto;
    padding-left: 15px;
    padding-right: 15px;
    text-align: center;
    width: 90%;
}

.jumbotron {
    background-color: #477bff;
    color: #fff;
    margin-bottom: 2rem;
    padding: 2rem 1rem;
    text-align: center;
}

.section {
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 0.5rem;
}

.section:hover {
    background-color: #f5f5f5;
    transition: color 2s ease-in-out, background-color 0.15s ease-in-out;
}

h1 {
    font-family: 'Montserrat', sans-serif;
    font-size: 48px;
}

button, input[type="submit"] {
    background-color: #d9edff;
    border: 1px solid transparent;
    border-radius: 0.25rem;
    font-size: 0.95rem;
    font-weight: 400;
    line-height: 1.5;
    padding: 0.375rem 0.75rem;
    text-align: center;
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    vertical-align: middle;
}

input[type="text"], input[type="number"] {
    line-height: 1.8;
    width: 25%;
}

input[type="text"]:hover, input[type="number"]:hover {
    background-color: #f5f5f5;
    transition: color 2s ease-in-out, background-color 0.15s ease-in-out;
}

table {
    background-color: transparent;
    margin-bottom: 1rem;
    width: 100%;
}

table th,
table td {
    padding: 0.75rem;
    vertical-align: middle;
}

tbody tr:nth-of-type(odd) {
    background-color: rgb(179, 208, 255, 0.3)
}
```
{% endspoiler %}