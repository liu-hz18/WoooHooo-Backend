import random
import json
import requests
from django.test import TestCase, Client

from .models import User
from .views import gen_response

CONTENT_TYPE = "application/json"

# Create your tests here.
class APITest(TestCase):
    """Main Test"""
    def setUp(self):
        self.check_user_signup("test", "123456", 200, "user was set successfully")

    def check_user_login(self, name, password, code, content):
        client = Client()
        response = client.get(f"/api/login?username={name}&userpass={password}")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], code)
        self.assertEqual(response_json["data"], content)

    def check_user_signup(self, name, password, code, content):
        client = Client()
        response = client.post("/api/login", data={"username": name, "userpass": password}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], code)
        self.assertEqual(response_json["data"], content)

    def test_gen_response(self):
        response = json.loads(gen_response(200, "123").content)
        self.assertEqual(response["code"], 200)
        self.assertEqual(response["data"], "123")

    def test_login_get(self):
        self.check_user_login("test", "123456", 200, "successful user validation")
        self.check_user_login("test", "", 400, "there is no username or password or None")
        self.check_user_login("test", "654321", 400, "password Error")
        self.check_user_login("testtesttesttest", "123456", 400, "username Error")

    def test_login_post(self):        
        self.check_user_signup("test", "654321", 400, "user is already existed")
        self.check_user_signup("test", None, 400, "there is no username or password")
        client = Client()
        response = client.post("/api/login", data="{123", content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "the data is not json")

    def check_validate(self, name, mail, code, content):
        client = Client()
        response = client.post("/api/validate", data={"username": name, "mail": mail}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], code)
        self.assertEqual(response_json["data"], content)

    def test_validate(self):
        validate_url = "/api/validate"
        client = Client()
        response = client.post(validate_url, data={"username": "liuhz", "mail": "liu-hz18@mails.tsinghua.edu.cn"}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertNotEqual(response_json["data"], "-1")
        
        response = client.get(validate_url)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "GET method not supported, please use POST")

        self.check_validate("liuhz", "liuhz", 400, "mail address format error")
        self.check_validate("", None, 400, "mail address or username error")

        response = client.post(validate_url, data="{123", content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "the data is not json")


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(name="lion", password="123456")
        User.objects.create(name="cat", password="654321")
 
    def test_user_db(self):
        """Animals that can speak are correctly identified"""
        lion = User.objects.get(name="lion")
        cat = User.objects.get(name="cat")
        self.assertEqual(lion.password, '123456')
        self.assertEqual(cat.password, '654321')
        self.assertEqual(str(lion), "lion")
        self.assertEqual(str(cat), "cat")
