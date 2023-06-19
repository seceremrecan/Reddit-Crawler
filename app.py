from flask import Flask, jsonify


from praw import Reddit
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Base, Post

app = Flask(__name__)



CLIENT_ID = 'HnuSMFN7tsJ1z8y4SUAxVw'
CLIENT_SECRET = 'ycQCCc0VndHVPpMDv9EYu95449Msrg'
USERNAME = 'seceremre'
PASSWORD = '258258258eE.'

# Reddit API'ye bağlanma
reddit = Reddit(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                username=USERNAME,
                password=PASSWORD,
                user_agent='defanceProject')

# PostgreSQL veritabanı bağlantısı oluşturma
DATABASE_URL = 'postgresql://postgres:258258258@localhost:5432/brandefance'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
@app.route('/', methods=['GET'])
def home():
    return 'Welcome to Reddit Crawler API'
# Tüm postları döndüren endpoint
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = session.query(Post).all()
    result = [{'id': post.id, 'title': post.title, 'subreddit': post.subreddit} for post in posts]
    return jsonify(result)

# Reddit API'ye istek atarak en son postları çeken endpoint
@app.route('/crawl', methods=['GET'])
def crawl_posts():
    subreddit_name = 'python'  # İstediğiniz subreddit'in adını buraya yazın
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.new(limit=10)  # En son 10 postu çekin

    for post in posts:
        new_post = Post(title=post.title, subreddit=subreddit_name)
        session.add(new_post)

    session.commit()
    return 'Posts crawled and saved successfully'

if __name__ == '__main__':
    
    app.run(debug=True)
Base.metadata.create_all(engine)    
