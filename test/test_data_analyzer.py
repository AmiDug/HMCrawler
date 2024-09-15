import unittest
from src.data_analyzer import return_price_average, return_rating_average, return_count_average

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.store_list = [
            {'price': 10, 'rate': 4, 'count': 100},
            {'price': 20, 'rate': 3, 'count': 200},
            {'price': 30, 'rate': 5, 'count': 300}
        ]
        self.empty_store_list = []

    def test_return_price_average(self):
        self.assertEqual(return_price_average(self.store_list), 20)
        self.assertEqual(return_price_average(self.empty_store_list), 0)

    def test_return_rating_average(self):
        self.assertEqual(return_rating_average(self.store_list), 4)
        self.assertEqual(return_rating_average(self.empty_store_list), 0)

    def test_return_count_average(self):
        self.assertEqual(return_count_average(self.store_list), 200)
        self.assertEqual(return_count_average(self.empty_store_list), 0)

if __name__ == '__main__':
    unittest.main()