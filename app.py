from flask import Flask, jsonify, redirect, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from models import Base, Post, User
import configparser
from flask_login import current_user
import time
import os

from playwright.sync_api import sync_playwright
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

config = configparser.ConfigParser()
config.read('.env')


db_host = os.getenv("DB_HOST", config['database']['host'])
db_user = os.getenv("DB_USER", config['database']['user'])
db_password = os.getenv("DB_PASSWORD", config['database']['password'])
db_name = os.getenv("DB_NAME", config['database']['database'])

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
engine = create_engine(DATABASE_URL)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@login_manager.user_loader
def load_user(user_id):
    return session.get(User, user_id)


@app.route('/', methods=['GET'])
def home():
    print('Welcome to Reddit Crawler API')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('crawl_posts'))

        flash('Invalid username or password')  # Flash a message to the user
        return redirect(url_for('login')) 
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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
        print('Kayıt işlemi başarılı. Artık giriş yapabilirsiniz.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/posts/<post_id>', methods=['GET'])
@login_required
def view_post(post_id):
    post = session.query(Post).get(post_id)
    if post:
        return redirect(post.url)
    else:
        flash('Post not found')
        return redirect(url_for('get_posts'))

@app.route('/posts', methods=['GET'])
@login_required
def get_posts():
    posts = session.query(Post).all()
    result = [{'id': post.id, 'title': post.title, 'subreddit': post.subreddit, 'url': post.url} for post in posts]
    return render_template('posts.html', posts=result)



@app.route('/crawl', methods=['GET'])
@login_required
def crawl_posts():
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page()

            subreddit_name = 'technology'
            page.goto(f'https://www.reddit.com/r/{subreddit_name}')
            posts = page.query_selector_all('.Post')

            session.query(Post).delete()
            session.commit()

            print('Veritabanı temizlendi.')

            for post in posts:
                ids = post.get_attribute('id')
                url_element = post.query_selector('a[data-click-id="body"]')
    
                if url_element is not None:
                    relative_url = url_element.get_attribute('href')
                    url = f"https://www.reddit.com{relative_url}"
                    title_element = url_element.query_selector('h3')
                    if title_element is not None:
                        title = title_element.inner_text()

                        # Benzersiz ID kontrolü
                        existing_post = session.query(Post).filter_by(id=ids).first()
                        if existing_post:
                            continue  # Aynı ID'ye sahip gönderi var, atla
                        else:
                            new_post = Post(id=ids, subreddit=subreddit_name, url=url, title=title)
                            session.add(new_post)

            session.commit()


            browser.close()

        return render_template('message.html', message='Posts crawled and saved successfully redirected to the post page')
    except Exception as e:
        session.rollback()
        print('Hata:', str(e))
        return str(e), 500




if __name__ == '__main__':
    Base.metadata.create_all(engine)
    scheduler = BackgroundScheduler()
    scheduler.add_job(crawl_posts, 'interval', minutes=1)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
