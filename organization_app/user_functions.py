import os
from db import db
from sqlalchemy.sql import text
from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex


def check_if_username_exists(username):
    username = request.form["username"]
    sql = text("SELECT 1 FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    db.session.commit()
    if result.fetchone():
        return True
    else:
        return False
    
def add_user(username, password_hash):
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":password_hash})
    db.session.commit()

def get_user_id(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    user_id = db.session.execute(sql, {"username":username}).fetchone()[0]
    return user_id

