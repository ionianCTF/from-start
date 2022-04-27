from scripts import database
import flask
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import bcrypt
import time

@contextmanager
def session_scope():
    s = get_session()
    s.expire_on_commit = False
    try:
        yield s
        s.commit()
    except:
        s.rollback()
    finally:
        s.close()

def get_session():
    return sessionmaker(bind=database.engine)()

def get_user():
    username = flask.session['username']
    session = get_session()
    user = session.query(database.User).filter(database.User.username.in_([username])).first()
    return user

def credentials_valid(username, password):
    session = get_session()
    user = session.query(database.User).filter(database.User.username.in_([username])).first()
    if user:
        return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
    else:
        return False

def username_exists(username):
    session = get_session()
    return session.query(database.User).filter(database.User.username.in_([username])).first()

def email_exists(email):
    session = get_session()
    return session.query(database.User).filter(database.User.email.in_([email])).first()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def add_user(username, password, email):
    session = get_session()
    u = database.User(username=username, password=password, email=email, confirmedEmail=False, vip=1, created=time.strftime('%Y-%m-%d %H:%M:%S'))
    session.add(u)
    session.commit()
    print('Successfully added user', username)

def change_user(**kwargs):
    username = flask.session['username']
    session = get_session()
    user = session.query(database.User).filter(database.User.username.in_([username])).first()
    for arg, val in kwargs.items():
        if val != "":
            setattr(user, arg, val)
    session.commit()
