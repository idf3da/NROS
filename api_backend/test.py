import unittest

from myapp import api_routes


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_product_type(self):
        product_type = api_routes.ProductTypesApi.get(1)
        self.assertEqual(product_type[0], {"product_type": {"id": 1, "name": "Salt", "price": 10, "volume": 1}})

    def test_get_product_types(self):
        product_types = api_routes.ListProductTypesApi.get()
        self.assertEqual(product_types[0], {"product_types": [{"id": 1, "name": "Salt", "price": 10, "volume": 1},
                                                             {"id": 2, "name": "Sugar", "price": 11, "volume": 1},
                                                             {"id": 3, "name": "Meat", "price": 1000, "volume": 100},
                                                             {"id": 4, "name": "Milk", "price": 250, "volume": 200},
                                                             {"id": 5, "name": "Bread", "price": 50, "volume": 150},
                                                             {"id": 6, "name": "Cheese", "price": 500, "volume": 250},
                                                             {"id": 7, "name": "Fish", "price": 900, "volume": None}]})


if __name__ == '__main__':
    unittest.main()
