from flask.ext.sqlalchemy import SQLAlchemy
from models import Users, Sites
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask import session

def check_logged_in():
    if 'username' in session:
        username=session['username']
        return username
    else:
        return False

def login(username, password):
    if db.session.query(Users).filter_by(username=username).first():
        user = db.session.query(Users).filter_by(username=username).first()
        password = user.password
        pw_hash = generate_password_hash(password)
        print password
        print pw_hash
        if check_password_hash(pw_hash, password):
            session['username'] = username
            return 1
        else:
            return 2
def usercreate(username, email, password):
    users = db.session.query(Users).all()
    for user in users:
        if user.username == username:
            return 2
        elif user.email == email:
            return 4
    else:
        pw_hash = generate_password_hash(password)
        user = Users(username=username, email=email, password=pw_hash, admin=False)
        db.session.add(user)
        db.session.commit()
        return 1
    return 3

      
            



