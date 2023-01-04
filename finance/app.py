import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from string import punctuation
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get users stocks and balance
    rows = db.execute(
        "SELECT * FROM portfolio WHERE userid = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?",
                      session["user_id"])
    cash = cash[0]["cash"]

    # Start sum
    totalV = cash

    # Get stocks info
    for row in rows:
        look = lookup(row["symbol"])
        row["name"] = look["name"]
        row["price"] = look["price"]
        row["total"] = row["price"] * row["shares"]

        # Update sum
        totalV += row["total"]

        # Convert prices to USD
        row["price"] = usd(row["price"])
        row["total"] = usd(row["total"])

    return render_template("index.html", rows=rows, cash=usd(cash), totalV=usd(totalV))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("missing shares", 400)

        else:
            # Lookup for symbol and shares
            symbol = request.form.get("symbol").upper()
            shares = request.form.get("shares")

            # Verify if shares is a valid number
            if not shares or shares.isalpha() or shares in set(punctuation) or float(shares).is_integer() == False or int(shares) <= 0:
                return apology("invalid number of shares", 400)

            # If symbol is invalid return error
            if lookup(symbol) == None:
                return apology("invalid symbol", 400)

            else:
                shares = int(shares)
                sharePrice = lookup(symbol)["price"]
                purchase = sharePrice * shares

                # Get user cash balance
                balance = db.execute(
                    "SELECT cash FROM users WHERE id = ?", session["user_id"])
                balance = balance[0]["cash"]
                remainder = balance - purchase

                # Check if user can afford the stock
                if remainder < 0:
                    return apology("insufficient funds", 403)

                # Query db for symbol
                row = db.execute("SELECT * FROM portfolio WHERE userid = ? AND symbol = ?",
                                 session["user_id"], symbol)

                # Check if user already have shares of company
                if len(row) == 0:
                    # Insert buy of stocks
                    db.execute("INSERT INTO portfolio (userid, symbol, shares) VALUES (?, ?, ?)",
                               session["user_id"], symbol, shares)

                    # Insert value on history
                    db.execute("INSERT INTO history (userid, symbol, shares, method, price) VALUES (?, ?, ?, 'Buy', ?)",
                               session["user_id"], symbol, shares, sharePrice)

                    # Update user cash
                    db.execute("UPDATE users SET cash = ? WHERE id = ?",
                               remainder, session["user_id"])

                else:
                    # Get number of shares that user already own
                    nOldShares = db.execute("SELECT shares FROM portfolio WHERE userid = ? AND symbol = ?",
                                            session["user_id"], symbol)
                    nOldShares = nOldShares[0]["shares"]

                    # Sum the number of shares
                    newShares = nOldShares + shares

                    # Insert in db new value
                    db.execute("INSERT INTO portfolio (userid, symbol, shares) VALUES (?, ?, ?)",
                               session["user_id"], symbol, newShares)

                    # Update user cash
                    db.execute("UPDATE users SET cash = ? WHERE id = ?",
                               remainder, session["user_id"])

                    # Insert value on history
                    db.execute("INSERT INTO history (userid, symbol, shares, method, price) VALUES (?, ?, ?, 'Buy', ?)",
                               session["user_id"], symbol, shares, sharePrice)

                return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Select all entrys from history
    rows = db.execute(
        "SELECT * FROM history WHERE userid = ?", session["user_id"])
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
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
    """ Change Password """

    if request.method == "POST":
        # Verify all forms was submitted
        if not request.form.get("oldPswd") or not request.form.get("newPswd") or not request.form.get("confirm"):
            return apology("missing old or new password", 400)

        # Define some vars
        oldPswd = request.form.get("oldPswd")
        newPswd = request.form.get("newPswd")
        confirm = request.form.get("confirm")

        # Select old password
        hashV = db.execute(
            "SELECT hash FROM users WHERE id = ?", session["user_id"])
        hashV = hashV[0]["hash"]

        # Check if old password is correct
        if not check_password_hash(hashV, oldPswd):
            return apology("old password incorrect", 400)

        # Verify if passwords match
        if newPswd != confirm:
            return apology("new passwords do not match", 400)

        # Generate hash and update in db
        hashV = generate_password_hash(confirm)
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   hashV, session["user_id"])

        return redirect("/logout")

    else:
        return render_template("password.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        else:
            quote = lookup(request.form.get("symbol"))

            if quote == None:
                return apology("invalid symbol", 400)

            quote["price"] = usd(quote["price"])
            return render_template("quote.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password and confirmation was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide and confirm password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username do not exists
        if len(rows) == 1:
            return apology("username already exists", 400)

        # Ensure passwords match
        elif request.form.get("password") == request.form.get("confirmation"):
            pswdHash = generate_password_hash(request.form.get("password"))
            db.execute(
                "INSERT INTO users(username,hash) VALUES(?,?)", request.form.get("username"), pswdHash)
            return redirect("/login")

        else:
            return apology("passwords do not match", 400)

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Define some vars
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))

        # Return error if not shares
        if not shares:
            return apology("must provide number of shares", 400)

        if not symbol:
            return apology("must provide valid stock symbol", 400)

        # More vars
        symbolStats = lookup(symbol)
        rows = db.execute("SELECT * FROM portfolio WHERE userid = ? AND symbol = ?",
                          session["user_id"], symbol)

        # Return error if user dont own stock
        if len(rows) <= 0:
            return apology("must provide valid stock symbol", 400)

        # Get current amount of shares
        nOldShares = rows[0]["shares"]

        # Verify if user can sell the number of stocks
        if shares > nOldShares:
            return apology("shares sold can't exceed shares owned", 400)

        # Get sold value
        soldV = symbolStats["price"] * shares

        # Add value to balance
        cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]
        cash = cash + soldV
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   cash, session["user_id"])
        # Update shares
        nNewShares = nOldShares - shares

        if nNewShares >= 1:
            db.execute("UPDATE portfolio SET shares = ? WHERE userid = ? AND symbol = ?",
                       nNewShares, session["user_id"], symbol)

        else:
            db.execute("DELETE FROM portfolio WHERE symbol = ? AND userid = ?",
                       symbol, session["user_id"])

        # Insert history
        db.execute("INSERT INTO history (userid, symbol, shares, method, price) VALUES (?, ?, ?, 'Sell', ?)",
                   session["user_id"], symbol, shares, symbolStats["price"])

        return redirect("/")
    else:
        # Get user stocks
        portfolio = db.execute("SELECT symbol FROM portfolio WHERE userid = ?",
                               session["user_id"])

        return render_template("sell.html", portfolio=portfolio)
