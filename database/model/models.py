from database.model import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey

class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable = False)
    nickname = Column(String(64))
    password = Column(String(50), nullable = False)
    