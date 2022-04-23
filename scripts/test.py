import database
from flask import session
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
    return sessionmaker(database.engine)()
 
def get_user():
    username = session['username']
    with session_scope() as s:
        user = s.query(database.User).filter(database.User.username.in_([username])).first()
        return user

def credentials_valid(username, password):
    with session_scope() as s:
        user = s.query(database.User).filter(database.User.username.in_([username])).first()
        if user:
            return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
        else:
            return False
 
def username_taken(username):
    with session_scope() as s:
        return s.query(database.User).filter(database.USer.username.in_([username])).first()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def add_user(username, password, email):
    with session_scope() as s:
        u = database.User(id=2, username=username, password=password, email=email, confirmedEmail=False, created=time.strftime('%Y-%m-%d %H:%M:%S'))
        s.add(u)
        s.commit()

password = hash_password('12345678')
add_user('hakihaki1', password, 'test@asdd.com')

username_taken('hakihaki')
