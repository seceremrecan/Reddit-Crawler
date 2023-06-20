import unittest
from app import app, session, Post
from models import User
from flask_login import login_user

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Kullanıcıyı var olan kullanıcı olarak kontrol et
        user = session.query(User).filter_by(username='test_user').first()

        if user is None:
            # Kullanıcı yoksa, yeni bir kullanıcı oluştur ve ekleyin
            user = User(username='test_user', password='test_password')
            user.set_password('test_password')  # Şifreyi ayarla
            session.add(user)
            session.commit()

        login_user(user)

def tearDown(self):
    # Kullanıcıyı veritabanından sil
    user = session.query(User).filter_by(username='test_user').first()

    if user is not None:
        session.delete(user)
        session.commit()

    def test_get_posts(self):
        # /posts endpoint'ini test etmek için gerekli kodları burada yazın
        # Beklenen sonuçları kontrol edin
        response = self.app.get('/posts', follow_redirects=True)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_crawl_posts(self):
        # /crawl endpoint'ini test etmek için gerekli kodları burada yazın
        # Beklenen sonuçları kontrol edin
        response = self.app.get('/crawl', follow_redirects=True)
        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, 'Posts crawled and saved successfully')

if __name__ == '__main__':
    unittest.main()