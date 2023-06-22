import unittest
from flask import Flask
from flask_login import LoginManager, login_user, current_user
from app import app, session, Post
from models import User
from werkzeug.security import generate_password_hash

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

       
        username = 'test_user'
        password = 'test_password'
        user = session.query(User).filter_by(username=username).first()

        if user is None:
            
            user = User(username=username, password=password)
            session.add(user)
            session.commit()

        
        with app.test_request_context('/'):   # test_request_context metodu ile bir HTTP isteği bağlamı oluşturuldu
           
            login_user(user)



    def tearDown(self):
        
        username = 'test_user'
        user = session.query(User).filter_by(username=username).first()

        if user is not None:
            session.delete(user)
            session.commit()

    def test_get_posts(self):
       
        username = 'test_user'
        password = 'test_password'
        user = session.query(User).filter_by(username=username).first()

        with app.test_request_context('/'):
            
            login_user(user)
            
            response = self.app.get('/posts')
            data = response.data.decode()  # Decode the response data

            self.assertEqual(response.status_code, 200)
            self.assertIn('/posts', data)  # Check if the response data contains the expected HTML template


    def test_crawl_posts(self):
        
        username = 'test_user'
        password = 'test_password'
        user = session.query(User).filter_by(username=username).first()

        with app.test_request_context('/'):
            
            login_user(user)
            
            response = self.app.get('/crawl')
            data = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Posts crawled and saved successfully redirected to the post page', data)


if __name__ == '__main__':
    unittest.main()
