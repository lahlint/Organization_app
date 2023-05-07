import os
from db import db
from sqlalchemy.sql import text
from secrets import token_hex


def add_entry(notes_id, entry, timestamp):
    sql = text("INSERT INTO entrys (notes_id, entry, timestamp) VALUES (:notes_id, :entry, :timestamp)")
    db.session.execute(sql, {"notes_id":notes_id , "entry":entry, "timestamp":timestamp})
    db.session.commit()

def get_entrys(notes_id):
    sql = text("SELECT entry, timestamp, e.id FROM entrys e LEFT JOIN notes n ON n.id=e.notes_id WHERE n.id=:notes_id ORDER BY e.id")
    result = db.session.execute(sql, {"notes_id":notes_id})
    entrys = result.fetchall()
    db.session.commit()
    return entrys