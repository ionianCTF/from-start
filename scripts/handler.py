from scripts import database
import flask
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager
import bcrypt
import time
import json
import string
import random

session = scoped_session(sessionmaker(bind=database.engine))

def get_user():
    username = flask.session['username']
    try:
        user = session.query(database.User).filter(database.User.username.in_([username])).first()
        return user
    except:
        session.rollback()
        raise

def credentials_valid(username, password):
    try:
        user = session.query(database.User).filter(database.User.username.in_([username])).first()
        if user:
            return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
        else:
            return False
    except:
        session.rollback()
        raise

def username_exists(username):
    try:
        return session.query(database.User).filter(database.User.username.in_([username])).first()
    except:
        session.rollback()
        raise

def email_exists(email):
    try:
        return session.query(database.User).filter(database.User.email.in_([email])).first()
    except:
        session.rollback()
        raise

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def add_user(username, password, email):
    u = database.User(username=username, password=password, email=email, confirmedEmail=False, vip=1, created=time.strftime('%Y-%m-%d %H:%M:%S'), invitationCode=create_random_code(session))
    session.add(u)
    try:
        session.commit()
    except:
        session.rollback()
        raise
    print('Successfully added user', username)

def change_user(**kwargs):
    username = flask.session['username']
    user = session.query(database.User).filter(database.User.username.in_([username])).first()
    for arg, val in kwargs.items():
        if val != "":
            setattr(user, arg, val)
    try:
        session.commit()
    except:
        session.rollback()
        raise

def create_random_code(session):
    try:
        chars=string.ascii_uppercase + string.digits
        size = 10
        code = ''.join(random.choice(chars) for _ in range(size))
        while session.query(database.User).filter(database.User.invitationCode.in_([code])).first():
            code = ''.join(random.choice(chars) for _ in range(size))
        return code
    except:
        session.rollback()
        raise

def get_user_data(username):
    try:
        user = json.loads(str(session.query(database.User).filter(database.User.username.in_([username])).first()))
        return user
    except:
        session.rollback()
        raise