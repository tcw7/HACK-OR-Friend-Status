from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))
    friends = db.relationship('Friend',backref='user',lazy=True )
    
    def __repr__(self):
        return '<User %r>' % self.username


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    friendname = db.Column(db.String(120), nullable=False)
    serviceidentifier = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    services = db.relationship('Service',backref='friend',lazy=True )
    
    def __repr__(self):
        return '<Friend %r>' % self.friendname
    
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servicename =  db.Column(db.String(120), nullable=False)
    servicestatus = db.Column(db.String(120), unique=True, nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('friend.id'), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.servicename

# Create tables.
Base.metadata.create_all(bind=engine)
