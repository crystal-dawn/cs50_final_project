from cs50 import SQL
from flask import Flask, render_template, request

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
    return render_template("login.html", show="show")

# Registration form
# @app.route('/', methods=["POST"])
# def register():
#     """ Register User """

#     if request.method == "POST":
#         username = request.form.get("registerUsername")
#         existingUsers = db.execute("SELECT * FROM users WHERE username = :username", username=username)
