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
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        valid_username = validate_username()
        valid_password = validate_password()

        if valid_username and valid_password:
            message = register_user(valid_username, valid_password)

            flash('Registration succesesful, please login', 'message')
            return redirect("/")

    return render_template("register.html")


# Add user to database
def register_user(valid_username, valid_password):
    hash = generate_password_hash(valid_password)

    db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=valid_username, hash=hash)

    return 'Registration successful, please login'


# Validate username
def validate_username():
    username = request.form.get("registerUsername")
    # Select existing users from database
    users = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    # Username validation
    if not username or not username.strip():
        flash('Name is missing', 'error')
    # Username already exists
    elif len(users):
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
