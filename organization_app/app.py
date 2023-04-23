from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    if session.get("username"):
        sql = text("SELECT id FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": session.get("username")})
        user_id = result.fetchone()[0]
        sql = text("SELECT name, id FROM lists WHERE user_id=:user_id")
        result = db.session.execute(sql, {"user_id":user_id})
        lists = result.fetchall()
        db.session.commit()
        return render_template("index.html", lists=lists) 
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/add_user", methods=["POST"])
def add_user():
    username = request.form["username"]
    sql = text("SELECT 1 FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    if result.fetchone():
        return render_template("error.html", message="Username already exists")
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
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
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": session.get("username")})
    user_id = result.fetchone()[0]
    print(user_id)
    sql = text("INSERT INTO lists (user_id, name) VALUES (:user_id, :name)")
    db.session.execute(sql, {"user_id": user_id, "name":list_name})
    db.session.commit()
    return redirect("/")

@app.route("/add_task", methods=["POST"])
def add_task():
    list_name = request.form["list"]
    task = request.form["task"]
    tasks = request.form["tasks"]
    sql = text("SELECT id FROM lists WHERE name=:name")
    result = db.session.execute(sql, {"name":list_name})
    list_id = result.fetchone()[0]
    sql = text("INSERT INTO tasks (list_id, task, status) VALUES (:list_id, :task, :status)")
    db.session.execute(sql, {"list_id":list_id , "task":task, "status":0})
    db.session.commit()
    return redirect("/list/"+str(list_id))

@app.route("/list/<list_id>")
def show_list(list_id):
    sql = text("SELECT name FROM lists WHERE id=:list_id")
    result = db.session.execute(sql, {"list_id":list_id})
    name = result.fetchone()[0]
    sql = text("SELECT task, status, t.id FROM tasks t LEFT JOIN lists l ON l.id=t.list_id WHERE name=:name AND status!=:status ORDER BY t.id")
    result = db.session.execute(sql, {"name":name, "status":2})
    tasks = result.fetchall()
    tasks2 = []
    for task in tasks:
        task = task[0]
        tasks2.append(task)
    db.session.commit()
    return render_template("list.html", list=name, tasks=tasks, list_id=list_id)

@app.route("/done", methods=["POST"])
def done():
    task = request.form["task"]
    list_id = request.form["list"]
    sql = text("UPDATE tasks SET status=:new_status WHERE id=:id")
    db.session.execute(sql, {"new_status":1, "id":task})
    db.session.commit()
    return redirect("/list/"+list_id)

@app.route("/undo", methods=["POST"])
def undo():
    task = request.form["task"]
    list_id = request.form["list"]
    sql = text("UPDATE tasks SET status=:new_status WHERE id=:id")
    db.session.execute(sql, {"new_status":0, "id":task})
    db.session.commit()
    return redirect("/list/"+list_id)

@app.route("/remove_tasks", methods=["POST"])
def remove_tasks():
    list_id = request.form["list"]
    sql = text("UPDATE tasks SET status=:new_status WHERE status=:status AND list_id=:list_id")
    db.session.execute(sql, {"new_status":2, "status":1, "list_id":list_id})
    db.session.commit()
    return redirect("/list/"+list_id)

@app.route("/remove_lists")
def remove_lists():
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": session.get("username")})
    user_id = result.fetchone()[0]
    sql = text("SELECT name, id FROM lists WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    lists = result.fetchall()
    db.session.commit()
    return render_template("remove_lists.html",lists=lists)

@app.route("/remove_list", methods=["POST"])
def remove_list():
    list_id = request.form["list_id"]
    sql = text("DELETE FROM lists WHERE id=:list_id")
    db.session.execute(sql, {"list_id":list_id})
    db.session.commit()
    return redirect("/remove_lists")