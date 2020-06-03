""" Flask testing module """
import requests, json, jsonpath, unittest

class TestCase(unittest.TestCase):
    """
        Tests
    """
    def test_api_tags_get_1(self):
        """
            Testing tags
        """
        response = requests.get("http://127.0.0.1:5000/api/tags", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'tags')
        page = p[0][0]
        self.assertEqual(page['id'], 1)
        self.assertEqual(page['minimum'], 10)
        self.assertEqual(page['capacity'], 200)

    def test_api_tags_get_2(self):
        """
            Testing tags
        """
        response = requests.get("http://127.0.0.1:5000/api/tags", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'tags')
        page = p[0][1]
        self.assertEqual(page['id'], 2)
        self.assertEqual(page['minimum'], 0)
        self.assertEqual(page['capacity'], 100)

    def test_api_tags_get_3(self):
        """
            Testing tags
        """
        response = requests.get("http://127.0.0.1:5000/api/tags", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'tags')
        page = p[0][2]
        self.assertEqual(page['id'], 3)
        self.assertEqual(page['minimum'], 0)
        self.assertEqual(page['capacity'], 100)

    def test_api_tags_post(self):
        """
            Testing tags
        """
        response = requests.post("http://127.0.0.1:5000/api/tags", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "No data")

#--------------------------------------------------------------

    def test_api_predict_get(self):
        """
            Testing predict
        """
        response = requests.get("http://127.0.0.1:5000/api/predict", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "Internal Server Error")

    def test_api_predict_post(self):
        """
            Testing predict
        """
        response = requests.post("http://127.0.0.1:5000/api/predict", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "The method is not allowed for the requested URL.")

#--------------------------------------------------------------

    def test_api_sales_get_1(self):
        """
            Testing sales
        """
        response = requests.get("http://127.0.0.1:5000/api/sales", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'sales')
        page = p[0][0]
        self.assertEqual(page['id'], "50")
        self.assertEqual(page['date'], "2012-02-28 00:05:23")
        self.assertEqual(page['count'], 10)
        self.assertEqual(page['point_id'], "12")

    def test_api_sales_get_2(self):
        """
            Testing sales
        """
        response = requests.get("http://127.0.0.1:5000/api/sales", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'sales')
        page = p[0][1]
        self.assertEqual(page['id'], "51")
        self.assertEqual(page['date'], "2012-01-28 00:05:23")
        self.assertEqual(page['count'], 10)
        self.assertEqual(page['point_id'], "12")

    def test_api_sales_get_3(self):
        """
            Testing sales
        """
        response = requests.get("http://127.0.0.1:5000/api/sales", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'sales')
        page = p[0][2]
        self.assertEqual(page['id'], "52")
        self.assertEqual(page['date'], "2012-01-28 00:05:23")
        self.assertEqual(page['count'], 10)
        self.assertEqual(page['point_id'], "13")

    def test_api_sales_get_4(self):
        """
            Testing sales
        """
        response = requests.get("http://127.0.0.1:5000/api/sales", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'sales')
        page = p[0][3]
        self.assertEqual(page['id'], "53")
        self.assertEqual(page['date'], "2012-02-28 00:05:23")
        self.assertEqual(page['count'], 10)
        self.assertEqual(page['point_id'], "13")

    def test_api_sales_post(self):
        """
            Testing sales
        """
        response = requests.post("http://127.0.0.1:5000/api/sales", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "No data")

#--------------------------------------------------------------

    def test_api_lstms_get_1(self):
        """
            Testing lstms
        """
        response = requests.get("http://127.0.0.1:5000/api/lstms", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'LSTMs')
        page = p[0][0]
        self.assertEqual(page['id'], 1)
        self.assertEqual(page['point_id'], "12")
        self.assertEqual(page['product_type_id'], "9")
    
    def test_api_lstms_get_2(self):
        """
            Testing lstms
        """
        response = requests.get("http://127.0.0.1:5000/api/lstms", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'LSTMs')
        page = p[0][1]
        self.assertEqual(page['id'], 2)
        self.assertEqual(page['point_id'], "13")
        self.assertEqual(page['product_type_id'], "9")

    def test_api_lstm_post(self):
        """
            Testing lstms
        """
        response = requests.post("http://127.0.0.1:5000/api/lstms", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "No data")

#--------------------------------------------------------------

    def test_api_points_get_1(self):
        """
            Testing points
        """
        response = requests.get("http://127.0.0.1:5000/api/points", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = json_response = json.loads(response.text)
        page = (p['points'])[0]
        self.assertEqual(page['id'], "12")
        self.assertEqual(page['address'], "adress1War")

    def test_api_points_get_2(self):
        """
            Testing points
        """
        response = requests.get("http://127.0.0.1:5000/api/points", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = json_response = json.loads(response.text)
        page = (p['points'])[1]
        self.assertEqual(page['id'], "13")
        self.assertEqual(page['address'], "adress1War")

    def test_api_points_post(self):
        """
            Testing points
        """
        response = requests.post("http://127.0.0.1:5000/api/points", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "No data")

#--------------------------------------------------------------

    def test_api_product_types_get_1(self):
        """
            Testing product types
        """
        response = requests.get("http://127.0.0.1:5000/api/product_types", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'product_types')
        page = p[0][0]
        self.assertEqual(page['id'], "0")
        self.assertEqual(page['name'], "Sugar")
        self.assertEqual(page['price'], 1000)

    def test_api_product_types_get_2(self):
        """
            Testing product types
        """
        response = requests.get("http://127.0.0.1:5000/api/product_types", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = jsonpath.jsonpath(json_response, 'product_types')
        page = p[0][1]
        self.assertEqual(page['id'], "9")
        self.assertEqual(page['name'], "Sugar")
        self.assertEqual(page['price'], 1000)

    def test_api_product_types_post(self):
        """
            Testing product types
        """
        response = requests.post("http://127.0.0.1:5000/api/product_types", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "No data")

#--------------------------------------------------------------

    def test_api_tags_id_0_get(self):
        """
            Testing tags id
        """
        response = requests.get("http://127.0.0.1:5000/api/tags/0", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.")

    def test_api_tags_id_0_post(self):
        """
            Testing tags id
        """
        response = requests.post("http://127.0.0.1:5000/api/tags/0", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "The method is not allowed for the requested URL.")

    def test_api_tags_id_1(self):
        """
            Testing tags id
        """
        response = requests.get("http://127.0.0.1:5000/api/tags/1", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = json_response = json.loads(response.text)
        page = p['tag']
        self.assertEqual(page['id'], 1)
        self.assertEqual(page['minimum'], 10)
        self.assertEqual(page['capacity'], 200)

    def test_api_tags_id_2(self):
        """
            Testing tags id
        """
        response = requests.get("http://127.0.0.1:5000/api/tags/2", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = json_response = json.loads(response.text)
        page = p['tag']
        self.assertEqual(page['id'], 2)
        self.assertEqual(page['minimum'], 0)
        self.assertEqual(page['capacity'], 100)

    def test_api_tags_id_3(self):
        """
            Testing tags id
        """
        response = requests.get("http://127.0.0.1:5000/api/tags/3", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = json_response = json.loads(response.text)
        page = p['tag']
        self.assertEqual(page['id'], 3)
        self.assertEqual(page['minimum'], 0)
        self.assertEqual(page['capacity'], 100)

    def test_api_tags_id_4(self):
        """
            Testing tags id
        """
        response = requests.get("http://127.0.0.1:5000/api/tags/4", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        p = json_response = json.loads(response.text)
        page = p['tag']
        self.assertEqual(page['id'], 4)
        self.assertEqual(page['minimum'], 0)
        self.assertEqual(page['capacity'], 1000)

#--------------------------------------------------------------

    def test_api_lstms_id_1(self):
            """
                Testing lstms id
            """
            response = requests.get("http://127.0.0.1:5000/api/lstms/1", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
            json_response = json.loads(response.text)
            p = json_response = json.loads(response.text)
            page = p['lstm']
            self.assertEqual(page['id'], 1)
            self.assertEqual(page['point_id'], "12")
            self.assertEqual(page['product_type_id'], "9")

    def test_api_lstms_id_2(self):
            """
                Testing lstms id
            """
            response = requests.get("http://127.0.0.1:5000/api/lstms/2", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
            json_response = json.loads(response.text)
            p = json_response = json.loads(response.text)
            page = p['lstm']
            self.assertEqual(page['id'], 2)
            self.assertEqual(page['point_id'], "13")
            self.assertEqual(page['product_type_id'], "9")

#--------------------------------------------------------------

    def test_api_user_integrate(self):
        """
            Testing user integrate
        """
        response = requests.get("http://127.0.0.1:5000/api/user/integrate", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "The method is not allowed for the requested URL.")

    def test_api_authentication_integrate(self):
        """
            Testing authentication integrate
        """
        response = requests.get("http://127.0.0.1:5000/api/authentication/integrate", headers = {"Authorization" : "036d20170acccf1f8ddbc4005810219bcff14321001a2a6f567ef3cf2091b7ee"})
        json_response = json.loads(response.text)
        self.assertEqual(json_response['message'], "The method is not allowed for the requested URL.")


if __name__ == '__main__':
    LOG = 'public/api_test.txt'
    file = open(LOG, 'w')
    runner = unittest.TextTestRunner(file)
    unittest.main(testRunner=runner)
    file.close()
