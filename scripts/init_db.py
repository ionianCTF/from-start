import sys
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# Local
SQLALCHEMY_DATABASE_URI = 'mysql://bc53e4e5b304e4:9d8c24da@eu-cdbr-west-02.cleardb.net/heroku_193f13a231d0e1b'

Base = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(SQLALCHEMY_DATABASE_URI)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    password = Column(String(512))
    email = Column(String(50), unique=True)
    confirmedEmail = Column(Boolean, unique=False, default=False)
    created = Column(Date)
    vip = Column(Integer)
    lastActive = Column(DateTime)
    invitationCode = Column(String(10), unique=True)
    picUrl = Column(String(10)),
    balance = Column(Float, default=0.00)
    taskProfit = Column(Float, default=0.00)
    invitationCommision = Column(Float, default=0.00)


    def __repr__(self):
        return {
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
            'invitationCommision': self.invitationCommision
        }

class Task(Base):
    __tablename__ = "task"
    
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'))
    social = Column(Integer)
    status = Column(Integer)
    created = Column(DateTime)
    duration = Column(Integer)
    requirements = Column(Integer)
    link = Column(String(64))
    submited = Column(DateTime)

    def __repr__(self):
        return {
            'id': self.id,
            'user': self.user,
            'social': self.social,
            'status': self.status,
            'created': self.created,
            'duration': self.duration,
            'requirements': self.requirements,
            'link': self.link,
            'submited': self.submited
        }

engine = db_connect()  # Connect to database
User.__table__.drop(engine) # Drop tables
Task.__table__.drop(engine)
Base.metadata.create_all(engine)  # Create models and tables
