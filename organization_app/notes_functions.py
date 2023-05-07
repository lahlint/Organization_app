import os
from db import db
from sqlalchemy.sql import text
from secrets import token_hex


def add_notes(notes_name, user_id):
    sql = text("INSERT INTO notes (user_id, name) VALUES (:user_id, :name)")
    db.session.execute(sql, {"user_id": user_id, "name":notes_name})
    db.session.commit()

def get_notes(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()[0]
    sql = text("SELECT name, id FROM notes WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    notes = result.fetchall()
    db.session.commit()
    return notes

def get_notes_name(notes_id):
    sql = text("SELECT name FROM notes WHERE id=:notes_id")
    result = db.session.execute(sql, {"notes_id":notes_id})
    notes_name = result.fetchone()[0]
    return notes_name

def get_notes_id(notes_name, user_id):
    sql = text("SELECT id FROM notes WHERE user_id=:user_id AND name=:notes_name")
    result = db.session.execute(sql, {"user_id":user_id, "notes_name":notes_name})
    notes_id = result.fetchone()[0]
    return notes_id

def check_if_notes_already_exists(notes_name, user_id):
    sql = text("SELECT 1 FROM notes WHERE name=:notes_name AND user_id=:user_id")
    result = db.session.execute(sql, {"notes_name":notes_name, "user_id":user_id})
    if result.fetchone():
        return True
    else:
        return False
    
def check_rights_to_notes(user_id, notes_id):
    sql = text("SELECT 1 FROM notes WHERE user_id=:user_id AND id=:notes_id")
    result = db.session.execute(sql, {"user_id":user_id, "notes_id":notes_id})
    if result.fetchone():
        return True
    else:
        return False
    
def delete_notes(notes_id):
    sql = text("DELETE FROM notes WHERE id=:notes_id")
    db.session.execute(sql, {"notes_id":notes_id})
    db.session.commit()