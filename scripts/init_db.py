import sys
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# Local
SQLALCHEMY_DATABASE_URI = 'mysql://b6bd5b14578f94:30a1b042@us-cdbr-east-05.cleardb.net/heroku_a38d37cd5653d5e'

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
    confirmedEmail= Column(Boolean, unique=False, default=True)
    created = Column(Date)
    vip = Column(Integer, ForeignKey('vip.id'))
    lastActive = Column(DateTime)
    invitationCode = Column(String(10))
    invitationCommision = Column(Float)

    def __repr__(self):
        return '<User %r>' % self.username

class Vip(Base):
    __tablename__ = "vip"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    daily = Column(Integer)
    cost = Column(Integer)

    def __repr__(self):
        return '<VIP %r>' % self.id
    
class Social(Base):
    __tablename__ = "social"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    color = Column(Integer)

    def __repr__(self):
        return '<Social %r>' % self.name

class Task(Base):
    __tablename__ = "task"
    
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'))
    social = Column(Integer, ForeignKey('social.id'))
    status = Column(Integer)
    created = Column(DateTime)
    duration = Column(Integer)
    requirements = Column(Integer)
    link = Column(String(64))
    submited = Column(DateTime)

    def __repr__(self):
        return '<Task %r>' % self.link

engine = db_connect()  # Connect to database
Base.metadata.create_all(engine)  # Create models
