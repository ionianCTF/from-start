import sys
import os
import json
import random
import helpers
from datetime import datetime, timedelta
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
    level = db.Column(db.Integer)
    lastActive = db.Column(db.DateTime)
    invitationCode = db.Column(db.String(10), unique=True)
    invitedFrom = db.Column(db.String(10), default='NOBODY')
    picUrl = db.Column(db.String(10))
    balance = db.Column(db.Float, default=0)

    def __init__(self, username, email, password, invitationCode, invitedFrom='NOBODY'):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.confirmedEmail = False
        self.created = created=datetime.now()
        self.level = 1
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
            'level': self.level,
            'lastActive': self.lastActive,
            'invitationCode': self.invitationCode,
            'invitedFrom': self.invitationCode,
            'invitationCommision': 0,#self.invitationCommision,
            'picUrl': self.picUrl,
            'balance': self.balance,
            'taskProfit': 0#self.taskProfit,
        }, indent=4, default=str, sort_keys=True)

class Task(db.Model):
    __tablename__ = "task"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    social = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    requirements = db.Column(db.Integer)
    link = db.Column(db.String(64))
    submited = db.Column(db.DateTime, default=None)

    def __init__(self, user_id, social, hours=3):
        self.user_id = user_id
        self.social = social
        self.status = 0
        self.created = datetime.now()
        self.duration = hours
        self.requirements = 1
        self.link = 'facebook.com'
        self.submited = None

    def __repr__(self):
        return '<Task %r>' % self.id

    def get_json(self):
        return json.dumps({
            'id': self.id,
            'user_id': self.user_id,
            'social': self.social,
            'status': self.status,
            'created': self.created,
            'duration': self.duration,
            'requirements': self.requirements,
            'link': self.link,
            'submited': self.submited
        }, indent=4, default=str, sort_keys=True)

def change_user_password(username, password):
    user = User.query.filter_by(username=username).first()
    user.password = generate_password_hash(password)
    db.session.commit()

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
    user = User(username=username, password=password, email=email, invitationCode=helpers.create_random_code(), invitedFrom=invitedFrom)
    #reward_referrer(invitedFrom)
    db.session.add(user)
    db.session.commit()

def add_task(username, social, hours=3):
    # Check if user is privileged to another task
    user = User.query.filter_by(username=username).first()
    today_done = len(get_user_tasks(username))
    if (user.level == 1 and today_done == 3) or \
           (user.level == 2 and today_done == 5) or \
           (user.level == 3 and today_done == 8) or \
           (user.level == 4 and today_done == 15) or \
           (user.level == 5 and today_done == 22) or \
           (user.level == 6 and today_done == 60):
        return 0
    else:
        task = Task(user_id=user.id, social=social, hours=hours)
        db.session.add(task)
        db.session.commit()
        helpers.set_interval(delete_task(task.id), 604800) # Week in seconds
        helpers.set_interval(timeout_task(task.id), 10800) # 3 hours in seconds
        return 1

def get_user_tasks(username):
    user = User.query.filter_by(username=username).first()
    tasks = Task.query.filter_by(user_id=user.id).all()
    daily_tasks = []
    # Query tasks where the created datetime is bigger than yesterday 
    yesterday = datetime.now() - timedelta(days = 1)
    tasks = []
    for task in Task.query.filter(Task.user_id == user.id, Task.created > yesterday).all():
        tasks.append(task.get_json())
    return tasks

def init_db():
    db.create_all()
    user = User('useruser', 'user@user.com', '12345678', '1234567890')
    db.session.add(user)
    db.session.commit()

def delete_task(id):
    Task.query.filter_by(id=id).delete()
    db.session.commit()

def update_task(id, status):
    Task.query.filter_by(id=id).status = status
    db.session.commit()

def timeout_task(id):
    task = Task.query.filter_by(id=id)
    if task.status == 0:
        task.delete()
        db.session.commit()