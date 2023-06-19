from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    subreddit = Column(String)

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', subreddit='{self.subreddit}')>"
