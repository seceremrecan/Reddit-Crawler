import unittest
from app import app, session, Post

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        # Test sonrasında veritabanından test postlarını temizleme
        session.query(Post).delete()
        session.commit()

    def test_get_posts(self):
        # /posts endpoint'ini test etmek için gerekli kodları burada yazın
        # Beklenen sonuçları kontrol edin
        response = self.app.get('/posts')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_crawl_posts(self):
        # /crawl endpoint'ini test etmek için gerekli kodları burada yazın
        # Beklenen sonuçları kontrol edin
        response = self.app.get('/crawl')
        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, 'Posts crawled and saved successfully')

if __name__ == '__main__':
    unittest.main()
