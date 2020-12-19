from cs50 import SQL
from flask import Flask, render_template, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
# Configure Application
# First argument is the name of the application's module or package,
# A single module uses _name_ so Flask knows where to look for templates/static files
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 to use SQLite database
db = SQL("sqlite:///youtine.db")

# Identify which URL should trigger function it remote add origin https://github.com/crystal-dawn/cs50_final_project.git
@app.route('/')
# Function is given name, used to generate URLs for a particular function
def login():
    # render the main page
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "GET":
        return render_template("register.html", error = error)

    # User reached route via POST (as by submitting a form via POST)
    else:
        password_is_valid = validate_password()
        # TODO: Replace 'register.html' with account page if there are no errors
        return validate_username() or validate_password() or render_template('register.html', error = None)

# Validate username
def validate_username():
    username = request.form.get("registerUsername")
    users = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    # Username validation
    if not username or not username.strip():
        return render_template('register.html', username_error = 'Name is missing')
    # Username already exists
    elif len(users):
        return render_template('register.html', username_error = 'Username unavailable')


# Validate password
def validate_password():
    password = request.form.get("choosePassword")
    password_confirmed = request.form.get("retypePassword") == password

    app.logger.info("password: %s", password)
    app.logger.info("confirmation: %s", password_confirmed)

    if not password:
        return render_template('register.html', password_error = "Choose an eight character password")
    return render_template('register.html', error = None)