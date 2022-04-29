import os
from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base

SQLALCHEMY_DATABASE_URI = 'mysql://b6bd5b14578f94:30a1b042@us-cdbr-east-05.cleardb.net/heroku_a38d37cd5653d5e'
engine = create_engine(SQLALCHEMY_DATABASE_URI, future=True, connect_args={'connect_timeout': 1000})
Base = declarative_base()

class User(Base):
    __table__ = Table('user', Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<User(name={0}, ) %r>' % self.username

class Vip(Base):
    __table__ = Table('vip', Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<User(name={0}, ) %r>' % self.id

class Task(Base):
    __table__ = Table('task', Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<User(name={0}, ) %r>' % self.id

class Social(Base):
    __table__ = Table('social', Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<User(name={0}, ) %r>' % self.id

Base.metadata.create_all(engine)
