from app import app
from db import db
from flask import render_template, request, redirect, session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex
import list_functions
import user_functions
import task_functions


@app.route("/")
def index():
    if session.get("username"):
        username = session.get("username")
        lists = list_functions.get_lists(username)
        return render_template("index.html", lists=lists) 
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.form["username"]
    username_exists = user_functions.check_if_username_exists(username)
    if username_exists:
        return render_template("error.html", message="Username already exists")
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    user_functions.add_user(username, hash_value)
    return redirect("/")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return render_template("error.html", message="Username does not exist")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            pass
        else:
            return render_template("error.html", message="Invalid password")
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/create_list")
def create_list():
    return render_template("create_list.html")

@app.route("/add_list", methods=["POST"])
def add_list():
    list_name = request.form["list_name"]
    username = session.get("username")
    user_id = user_functions.get_user_id(username)
    list_exists = list_functions.check_if_list_already_exists(list_name, user_id)
    if list_exists:
        return render_template("error.html", message="A list with this name already exists")
    list_functions.add_list(list_name, user_id)
    return redirect("/")

@app.route("/add_task", methods=["POST"])
def add_task():
    list_name = request.form["list"]
    task = request.form["task"]
    list_id = list_functions.get_list_id(list_name)
    task_functions.add_task(list_id, task)
    return redirect("/list/" + str(list_id))

@app.route("/list/<list_id>")
def show_list(list_id):
    username = session.get("username")
    user_id = user_functions.get_user_id(username)
    rights = list_functions.check_rights_to_list(user_id, list_id)
    if not rights:
        return render_template("error.html", message="No rights to view this list")
    list_name = list_functions.get_list_name(list_id)
    tasks = task_functions.get_tasks(list_name)
    return render_template("list.html", list=list_name, tasks=tasks, list_id=list_id)

@app.route("/done", methods=["POST"])
def done():
    task_id = request.form["task"]
    list_id = request.form["list"]
    task_functions.mark_task_done(task_id)
    return redirect("/list/" + list_id)

@app.route("/undo", methods=["POST"])
def undo():
    task_id = request.form["task"]
    list_id = request.form["list"]
    task_functions.mark_task_undone(task_id)
    return redirect("/list/" + list_id)

@app.route("/remove_tasks", methods=["POST"])
def remove_tasks():
    list_id = request.form["list"]
    task_functions.remove_tasks(list_id)
    return redirect("/list/" + list_id)

@app.route("/remove_lists")
def remove_lists():
    username = session.get("username")
    lists = list_functions.get_lists(username)
    return render_template("remove_lists.html", lists=lists)

@app.route("/remove_list", methods=["POST"])
def remove_list():
    list_id = request.form["list_id"]
    list_functions.delete_list(list_id)
    return redirect("/remove_lists")