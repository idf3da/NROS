import unittest

from myapp import api_routes


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_product_type(self):
        product_type = api_routes.ProductTypesApi.get(1)
        self.assertEqual(product_type[0], {
            "product_type": {"id": 1, "name": "Salt", "price": 10,
                             "seasonality": 0}})

    def test_get_product_types(self):
        product_types = api_routes.ListProductTypesApi.get()
        self.assertEqual(product_types[0], {"product_types": [
            {"id": 1, "name": "Salt", "price": 10, "seasonality": 0},
            {"id": 2, "name": "Sugar", "price": 11, "seasonality": 0},
            {"id": 3, "name": "Meat", "price": 1000, "seasonality": 0},
            {"id": 4, "name": "Milk", "price": 250, "seasonality": 0},
            {"id": 5, "name": "Bread", "price": 50, "seasonality": 0},
            {"id": 6, "name": "Cheese", "price": 500, "seasonality": 0},
            {"id": 7, "name": "Fish", "price": 900, "seasonality": 0}]})


if __name__ == '__main__':
    log = 'public/api_test.txt'
    file = open(log, 'w')
    runner = unittest.TextTestRunner(file)
    unittest.main(testRunner=runner)
    file.close()
