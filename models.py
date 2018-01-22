from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from config import *


class Users(db.Model):
    __tablename__ = "user"
    id          = db.Column(db.Integer, primary_key = True)
    username    = db.Column(db.String)
    email       = db.Column(db.String)
    password    = db.Column(db.String)
    admin       = db.Column(db.Boolean)
    sites       = relationship("Sites", back_populates="user")
class Sites(db.Model):
    __tablename__ = "sites"
    id          = db.Column(db.Integer, primary_key = True)
    user_id     = db.Column(Integer, ForeignKey('user.id'))
    user        = relationship("Users", back_populates="sites")
    sitename    = db.Column(db.String)


def db_build():

    engine = create_engine(SQLALCHEMY_DATABASE_UR)
    if not database_exists(engine.url):
        create_database(engine.url)
        print("db created")
        db.create_all()
        
        db.session.commit()
 
    print(database_exists(engine.url))
    





