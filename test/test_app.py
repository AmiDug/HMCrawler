import unittest
from src.app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_echo_input(self):
        response = self.app.post('/echo_user_input', data=dict(user_input='test'))
        self.assertEqual(response.status_code, 200)

    def test_main_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)  # Assuming main.html contains <html> tag

if __name__ == '__main__':
    unittest.main()