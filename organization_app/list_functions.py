import os
from db import db
from sqlalchemy.sql import text
from secrets import token_hex


def get_lists(username):    
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()[0]
    sql = text("SELECT name, id FROM lists WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    lists = result.fetchall()
    db.session.commit()
    return lists

def add_list(list_name, user_id):
    sql = text("INSERT INTO lists (user_id, name) VALUES (:user_id, :name)")
    db.session.execute(sql, {"user_id": user_id, "name":list_name})
    db.session.commit()

def get_list_id(list_name):
    sql = text("SELECT id FROM lists WHERE name=:name")
    result = db.session.execute(sql, {"name":list_name})
    list_id = result.fetchone()[0]
    db.session.commit()
    return list_id

def get_list_name(list_id):
    sql = text("SELECT name FROM lists WHERE id=:list_id")
    result = db.session.execute(sql, {"list_id":list_id})
    name = result.fetchone()[0]
    db.session.commit()
    return name

def delete_list(list_id):
    sql = text("DELETE FROM lists WHERE id=:list_id")
    db.session.execute(sql, {"list_id":list_id})
    db.session.commit()

def check_if_list_already_exists(list_name, user_id):
    sql = text("SELECT 1 FROM lists WHERE name=:list_name AND user_id=:user_id")
    result = db.session.execute(sql, {"list_name":list_name, "user_id":user_id})
    if result.fetchone():
        return True
    else:
        return False
    
def check_rights_to_list(user_id, list_id):
    sql = text("SELECT 1 FROM lists WHERE user_id=:user_id AND id=:list_id")
    result = db.session.execute(sql, {"user_id":user_id, "list_id":list_id})
    if result.fetchone():
        return True
    else:
        return False