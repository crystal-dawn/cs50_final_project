import requests

from flask import Flask, flash, session, request, redirect, url_for, render_template
from functools import wraps
from cs50 import SQL


def is_existing_user(username: str, db):
    """Check if username exists within the database"""
    return db.execute("SELECT * FROM users WHERE username = :username", username=username)


def login_required(f):
    """Login Required Decorator

    https://flask.palletsprojects.com/en/1.0.x/patterns/viewdecorators/#login-required-decorator
    """
    # Wrap original function since it's replaced
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return render_template("layout.html")
        return f(*args, **kwargs)
    return decorated_function