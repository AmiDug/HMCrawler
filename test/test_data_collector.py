import unittest
from unittest.mock import patch
from flask_testing import TestCase
from src.data_collector import fetch_store, Store, db, app, populate_db, return_store

class TestBase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_store.sqlite3'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()
        populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestFetchStore(unittest.TestCase):
    @patch('src.data_collector.requests.get')
    def test_fetch_store(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = [{'id': 1, 'title': 'Test Product'}]
        result = fetch_store()
        self.assertEqual(result, [{'id': 1, 'title': 'Test Product'}])

class TestStoreModel(unittest.TestCase):
    def test_store_model(self):
        store = Store(id=1, title='Test Product', price=10.0, description='Test Description', category='Test Category',
                      image='test.jpg', rate=4.5, count=10)
        self.assertEqual(store.id, 1)
        self.assertEqual(store.title, 'Test Product')
        self.assertEqual(store.price, 10.0)
        self.assertEqual(store.description, 'Test Description')
        self.assertEqual(store.category, 'Test Category')
        self.assertEqual(store.image, 'test.jpg')
        self.assertEqual(store.rate, 4.5)
        self.assertEqual(store.count, 10)

class TestPopulateDB(TestBase):
    def test_populate_db(self):
        products = Store.query.all()
        self.assertGreater(len(products), 0)

class TestReturnStore(TestBase):
    def test_return_store(self):
        result = return_store('Fjallraven')
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]['title'], 'Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops')

if __name__ == '__main__':
    unittest.main()