import sys
import os
import json
import string
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(512))
    email = db.Column(db.String(50), unique=True)
    confirmedEmail = db.Column(db.Boolean, unique=False, default=False)
    created = db.Column(db.Date)
    vip = db.Column(db.Integer)
    lastActive = db.Column(db.DateTime)
    invitationCode = db.Column(db.String(10), unique=True)
    picUrl = db.Column(db.String(10))
    balance = db.Column(db.Float, default=0)
    tasksCompleted = db.Column(db.Integer, default=0)
    taskProfit = db.Column(db.Float, default=0)
    invitationCommision = db.Column(db.Float, default=0)

    def __init__(self, username, email, password, invitationCode, invitedFrom):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.confirmedEmail = False
        self.created = created=datetime.now()
        self.vip = 1
        self.multiplier = 0.5
        self.lastActive = created=datetime.now()
        self.invitationCode = invitationCode
        self.invitedFrom = invitedFrom
        self.picUrl = 'none'
        self.balance = 0

    def __repr__(self):
        return '<User %r>' % self.username
    
    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def get_json(self):
        return json.dumps({
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'confirmedEmail': self.confirmedEmail,
            'created': self.created,
            'vip': self.vip,
            'lastActive': self.lastActive,
            'invitationCode': self.invitationCode,
            'invitationCommision': self.invitationCommision,
            'picUrl': self.picUrl,
            'balance': self.balance,
            'taskProfit': self.taskProfit,
        }, indent=4, default=str, sort_keys=True)

class Task(db.Model):
    __tablename__ = "task"
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    social = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    requirements = db.Column(db.Integer)
    link = db.Column(db.String(64))
    submited = db.Column(db.DateTime)

    def __repr__(self):
        return '<Task %r>' % self.id

    def get_json(self):
        return json.dumps({
            'id': self.id,
            'user': self.user,
            'social': self.social,
            'status': self.status,
            'created': self.created,
            'duration': self.duration,
            'requirements': self.requirements,
            'link': self.link,
            'submited': self.submited
        })
    
def get_user_data(username):
    return User.query.filter_by(username=username).first().get_json()

def credentials_valid(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.validate_password(password)
    return False

def username_exists(username):
    return User.query.filter_by(username=username).first()

def email_exists(email):
    return User.query.filter_by(email=email).first()

def add_user(username, password, email):
    user = User(username=username, password=password, email=email, invitationCode=create_random_code())
    db.session.add(user)
    db.session.commit()

def create_random_code():
    chars=string.ascii_uppercase + string.digits
    size = 10
    code = ''.join(random.choice(chars) for _ in range(size))
    while User.query.filter_by(invitationCode=code).first():
        code = ''.join(random.choice(chars) for _ in range(size))
    return code

def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()