from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from apscheduler.schedulers.background import BackgroundScheduler
from praw import Reddit
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from models import Base, Post, User
import configparser

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

login_manager = LoginManager()
login_manager.init_app(app)

config = configparser.ConfigParser()
config.read('config.ini')

# Reddit API'ye bağlanma
reddit = Reddit(client_id=config['reddit']['client_id'],
                client_secret=config['reddit']['client_secret'],
                username=config['reddit']['username'],
                password=config['reddit']['password'],
                user_agent='defanceProject')

# PostgreSQL veritabanı bağlantısı oluşturma
DATABASE_URL = config['database']['url']

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to Reddit Crawler API'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))

        return 'Invalid username or password'

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return 'Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir kullanıcı adı deneyin.'

        new_user = User(username=username, password=password)
        session.add(new_user)
        session.commit()

        return 'Kayıt işlemi başarılı. Artık giriş yapabilirsiniz.'

    return render_template('register.html')

@app.route('/posts', methods=['GET'])
@login_required
def get_posts():
    posts = session.query(Post).all()
    result = [{'id': post.id, 'title': post.title, 'subreddit': post.subreddit} for post in posts]
    return jsonify(result)

@app.route('/crawl', methods=['GET'])
@login_required
def crawl_posts():
    try:
        subreddit_name = 'python'
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.new(limit=10)

        for post in posts:
            if session.query(Post).get(post.id) is None:
                new_post = Post(id=post.id, title=post.title, subreddit=subreddit_name)
                session.add(new_post)

        session.commit()
        return 'Posts crawled and saved successfully'
    except Exception as e:
        session.rollback()
        return str(e), 500

def fetch_posts():
    try:
        subreddit_name = 'python'
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.new(limit=10)

        for post in posts:
            new_post = Post(id=post.id, title=post.title, subreddit=subreddit_name)
            session.add(new_post)

        session.commit()
        print('Posts crawled and saved successfully')
    except Exception as e:
        session.rollback()
        print(f"Error while fetching posts: {str(e)}")

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_posts, 'interval', minutes=1)
scheduler.start()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
