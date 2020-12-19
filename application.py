from cs50 import SQL
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
# Configure Application
# First argument is the name of the application's module or package,
# A single module uses _name_ so Flask knows where to look for templates/static files
app = Flask(__name__)

### From CS50 Finance starter code 2020 ###
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
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


# Identify which URL should trigger function it remote add origin https://github.com/crystal-dawn/cs50_final_project.git
@app.route('/')
# Function is given name, used to generate URLs for a particular function
def login():
    # render the main page
    return render_template("layout.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "GET":
        return render_template("register.html", error=error)

    # User reached route via POST (as by submitting a form via POST)
    else:
        is_password_valid = validate_password()
        is_username_valid = validate_username()

        if is_username_valid:
            flash(is_username_valid, 'error')
        if is_password_valid:
            flash(is_password_valid, 'error')
        else:
            return redirect(url_for('register'))

        return render_template('register.html')


# Validate username
def validate_username():
    username = request.form.get("registerUsername")
    # Select existing users from database
    users = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    # Username validation
    if not username or not username.strip():
        return 'Name is missing'
    # Username already exists
    elif len(users):
        return 'Username unavailable'


# Validate password
def validate_password():
    password = request.form.get("choosePassword")
    password_confirmed = request.form.get("retypePassword") == password

    app.logger.info("password: %s", password)
    app.logger.info("confirmation: %s", password_confirmed)

    if not password:
        return "Choose an eight character password"
    return None