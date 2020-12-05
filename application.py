from cs50 import SQL
from flask import Flask, render_template

# Configure Application
# First argument is the name of the application's module or package,
# A single module uses _name_ so Flask knows where to look for templates/static files
app = Flask(__name__)

# Identify which URL should trigger functiongit remote add origin https://github.com/crystal-dawn/cs50_final_project.git
@app.route("/")
# Function is given name, used to generate URLs for a particular function
def index():
    # render the homepage
    return render_template("index.html")