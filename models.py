from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'

    @property
    def is_active(self):
        return True
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(150), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username is required.')
        return username

class Post(Base):
    __tablename__ = 'posts'
    

    id = Column(String(50), primary_key=True)
    title = Column(String(300))
    subreddit = Column(String(50))
    url = Column(String(500)) # <--- Add this line
    
