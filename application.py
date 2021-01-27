from cs50 import SQL
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import *
# Configure Application
# First argument is the name of the application's module or package,
# A single module uses _name_ so Flask knows where to look for templates/static files
app = Flask(__name__)

### From CS50 Finance starter code 2020 ###
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 to use SQLite database
db = SQL("sqlite:///youtine.db")

@app.route("/")
@login_required
def index():
    """Show Today's YouTine list"""
    return render_template("layout.html")


@app.route('/login', methods=["POST"])
def login():
    """Login form for existing users"""
    username = request.form.get("loginUsername")
    app.logger.info(username)
    # Check if username entered is in database
    if not is_existing_user(username, db):
        flash("Username does not exist", "message")
        return redirect("/")
        # Check that password entered matches to username enter record


    return render_template("layout.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "GET":
        return render_template("register.html")

    else:
        valid_username = validate_username()
        valid_password = validate_password()

        if valid_username and valid_password:
            message = register_user(valid_username, valid_password)

            flash('Registration successful, please login', 'message')
            return redirect("/")

    return render_template("register.html")


def register_user(valid_username, valid_password):
    """Add user to database"""
    hashedPassword = generate_password_hash(valid_password)

    db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=valid_username, hash=hashedPassword)

    return 'Registration successful, please login'


def validate_username():
    """Validate username for registration"""
    username = request.form.get("registerUsername")

    # Username validation
    if not username or not username.strip():
        flash('Name is missing', 'error')
    # Username already exists
    elif len(is_existing_user(username, db)):
        flash('Username unavailable', 'error')
    else:
        return username

# Validate password
def validate_password():
    password = request.form.get("choosePassword")
    password_confirmed = request.form.get("retypePassword") == password

    if not password:
        flash('Choose an eight character password', 'error')
    elif not password_confirmed:
        flash('Passwords much match', 'error')
    else:
        return password


# Add user to database
def register_user(valid_username, valid_password):
    hash = generate_password_hash(valid_password)

    db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=valid_username, hash=hash)

    return 'Registration successful, please login'
