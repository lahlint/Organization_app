import os
from db import db
from sqlalchemy.sql import text
from secrets import token_hex


def add_task(list_id, task):
    sql = text("INSERT INTO tasks (list_id, task, status) VALUES (:list_id, :task, :status)")
    db.session.execute(sql, {"list_id":list_id , "task":task, "status":0})
    db.session.commit()

def get_tasks(list_name):
    sql = text("SELECT task, status, t.id FROM tasks t LEFT JOIN lists l ON l.id=t.list_id WHERE name=:name AND status!=:status ORDER BY t.id")
    result = db.session.execute(sql, {"name":list_name, "status":2})
    tasks = result.fetchall()
    db.session.commit()
    return tasks

def mark_task_done(task_id):
    sql = text("UPDATE tasks SET status=:new_status WHERE id=:id")
    db.session.execute(sql, {"new_status":1, "id":task_id})
    db.session.commit()

def mark_task_undone(task_id):
    sql = text("UPDATE tasks SET status=:new_status WHERE id=:id")
    db.session.execute(sql, {"new_status":0, "id":task_id})
    db.session.commit()

def remove_tasks(list_id):
    sql = text("UPDATE tasks SET status=:new_status WHERE status=:status AND list_id=:list_id")
    db.session.execute(sql, {"new_status":2, "status":1, "list_id":list_id})
    db.session.commit()
