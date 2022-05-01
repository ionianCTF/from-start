import os
import json
from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base

SQLALCHEMY_DATABASE_URI = 'mysql://bc53e4e5b304e4:9d8c24da@eu-cdbr-west-02.cleardb.net/heroku_193f13a231d0e1b'
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'connect_timeout': 1000, 'pool_timeout': 20, 'pool_recycle': 299})
Base = declarative_base()

class User(Base):
    __table__ = Table('user', Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
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
            'invitationCommision': self.invitationCommision
        }, indent=4, sort_keys=True, default=str)

class Task(Base):
    __table__ = Table('task', Base.metadata, autoload=True, autoload_with=engine)

    def __repr__(self):
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
        }, indent=4, sort_keys=True, default=str)

Base.metadata.create_all(engine)
