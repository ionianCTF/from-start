import os
import time
import sqlalchemy as sql
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Boolean, Date, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orn import column_propery

SQLALCHEMY_DATABASE_URI = 'mysql://b6bd5b14578f94:30a1b042@us-cdbr-east-05.cleardb.net/heroku_a38d37cd5653d5e'

engine = create_engine(SQLALCHEMY_DATABASE_URI, future=True)

Base = declarative_base()

class User(Base):
    __table__ = Table('user', Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<User(name={0}, ) %r>' % self.username



class Vip(Base):
    __table__ = Table('vip', Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<User(name={0}, ) %r>' % self.username

class Task(Base):
    __table__ = Table('task', Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<User(name={0}, ) %r>' % self.username

class Social(Base):
    __table__ = Table('social', Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
        return '<User(name={0}, ) %r>' % self.username



Base.metadata.create_all(engine)
#Session = sql.orm.sessionmaker(engine)
#session = Session()

#user = User(id=1, username='test',password='sdasd',email='email', confirmedEmail=False, vip=1, created=time.strftime('%Y-%m-%d %H:%M:%S'))

#session.add(user)
#session.commit()
