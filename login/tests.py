import json
import requests
from django.test import TestCase, Client

from .models import User, BrowseHistory, SearchHistory, KeyWord
from .views import gen_response
from .utils import extract_keywords

CONTENT_TYPE = "application/json"
NOT_JSON = "the data is not json"
USER_NAME_NONE = "user name should not be None or blank"

# Create your tests here.
class APITest(TestCase):
    """Main Test"""
    def setUp(self):
        self.check_user_signup("test", "123456", 200, "user was set successfully")

    def check_user_login(self, name, passw, code, content):
        client = Client()
        response = client.get(f"/api/login?username={name}&userpass={passw}")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], code)
        self.assertEqual(response_json["data"], content)

    def check_user_signup(self, name, passw, code, content):
        client = Client()
        response = client.post("/api/login", data={"username": name, "userpass": passw}, content_type=CONTENT_TYPE)
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
        self.check_user_signup("test"*100, "654321", 400, "user name is too long")
        client = Client()
        response = client.post("/api/login", data="{123", content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], NOT_JSON)

        api_check = "/api/check"
        response = client.post(api_check, data={"username": "test"}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(response_json["data"], 'error')

        response = client.post(api_check, data={"username": "test123456"}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(response_json["data"], 'ok')

        response = client.post(api_check, data={"username": ""}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], 'there is no username')

        response = client.post(api_check, data="{name: ", content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], NOT_JSON)


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
        self.assertEqual(response_json["data"], NOT_JSON)

    def test_update(self):
        update_url = "/api/update"
        client = Client()
        response = client.post(update_url, data={"username": "test", "userpass": "654321"}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(response_json["data"], "user was set successfully")
        self.check_user_login("test", "654321", 200, "successful user validation")

        response = client.post(update_url, data="{123", content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], NOT_JSON)

        response = client.post(update_url, data={"username": "", "userpass": "654321"}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "there is no username or password")

        response = client.post(update_url, data={"username": "a"*10, "userpass": "654321"}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "user don't exist")

        response = client.post(update_url, data={"username": "test", "userpass": "a"*1000}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "passward is too long")


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(name="lion", pwhash="123456")
        User.objects.create(name="cat", pwhash="654321")
 
    def test_user_db(self):
        """Animals that can speak are correctly identified"""
        lion = User.objects.get(name="lion")
        cat = User.objects.get(name="cat")
        self.assertEqual(lion.pwhash, '123456')
        self.assertEqual(cat.pwhash, '654321')
        self.assertEqual(str(lion), "lion")
        self.assertEqual(str(cat), "cat")


class SearchHistoryTest(TestCase):
    def setUp(self):
        User.objects.create(name="test", pwhash="123456")
        User.objects.create(name="test_his", pwhash="654321")
        user = User.objects.filter(name="test").first()
        SearchHistory.objects.create(user=user, content="test content1")
        SearchHistory.objects.create(user=user, content="test content2")

    def test_add_history(self):
        search_log_url = "/api/searchhis"
        client = Client()
        response = client.post(search_log_url, data={"username": "test_his", "data": "新闻"}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(response_json["data"], "searching history logged successfully")
        
        response = client.post(search_log_url, data={"username": "test_his"}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "username or search content is None!")

        response = client.post(search_log_url, data={"username": "test_his1", "data": "新闻"}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "username don't exist.")

        response = client.post(search_log_url, data={"username": "test_his", "data": "a"*200}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "search content length is too long")

        response = client.post(search_log_url, data="{123", content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], NOT_JSON)

    def test_read_history(self):
        client = Client()
        response = client.get("/api/searchhis?username=test")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(response_json["data"], ["test content2", "test content1"])
        self.assertEqual(int(response_json["total"]), 2)

        response = client.get("/api/searchhis")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], USER_NAME_NONE)


class BrowseHistoryTest(TestCase):
    def setUp(self):
        User.objects.create(name="test", pwhash="123456")
        User.objects.create(name="test_his", pwhash="654321")
        user = User.objects.filter(name="test").first()
        BrowseHistory.objects.create(
            user=user, uid="123456", title="test title1", imgurl="",
            link="", source="", time="", content=""

        )
        BrowseHistory.objects.create(
            user=user, uid="654321", title="test title2", imgurl="",
            link="", source="", time="", content=""
        )

    def test_add_history(self):
        browse_log_url = "/api/browsehis"
        newsinfo = {'uid': "123", 'title': "This is a content", 'content': "1", 'imgurl': "1", 'source': "1", 'time': "1", 'link': "1"}
        client = Client()
        response = client.post(browse_log_url, data={"username": "test_his", "newsinfo": newsinfo}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        print(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(response_json["data"], "browsing history logged successfully")

        newsinfo["uid"] = "321"
        response = client.post(browse_log_url, data={"username": "test_his", "newsinfo": json.dumps(newsinfo)}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(response_json["data"], "browsing history logged successfully")
        
        newsinfo1 = {"uid": "123", "title": "This is a content", "content": "a"*500, "imgurl": "1", "source": "1", "time": "1", "link": "1"}
        response = client.post(browse_log_url, data={"username": "test_his", "newsinfo": newsinfo1}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "news info length is too long")

        response = client.post(browse_log_url, data={"username": "test_his"}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "username or newsinfo is None!")

        response = client.post(browse_log_url, data={"username": "test_his1", "newsinfo": newsinfo}, content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "username don't exist.")

        response = client.post(browse_log_url, data="{123", content_type=CONTENT_TYPE)
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], NOT_JSON) 

    def test_read_history(self):
        client = Client()
        response = client.get("/api/browsehis?username=test")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(response_json["data"], [
            {
                "uid": "654321",
                "title": "test title2",
                "imgurl": "",
                "content": "",
                "link": "",
                "source": "",
                "time": "",
            },
            {
                "uid": "123456",
                "title": "test title1",
                "imgurl": "",
                "content": "",
                "link": "",
                "source": "",
                "time": "",
            },
        ])
        self.assertEqual(int(response_json["total"]), 2)

        response = client.get("/api/browsehis")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], USER_NAME_NONE)


class KeyWordTest(TestCase):
    def setUp(self):
        User.objects.create(name="test", pwhash="123456")
        User.objects.create(name="test1", pwhash="654321")
        user = User.objects.filter(name="test").first()
        key1 = KeyWord.objects.create(keyword="新闻")
        key1.user.set([user])
        key2 = KeyWord.objects.create(keyword="美国")
        key2.user.set([user])

    def test_get_recommand(self):
        client = Client()
        response = client.get("/api/recommend?username=test&number=10&page=0")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(len(response_json["data"]), 10)
        self.assertIsNotNone(response_json["total"])

        response = client.get("/api/recommend?username=test1&number=10&page=0")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(len(response_json["data"]), 10)
        self.assertIsNotNone(response_json["total"])

        response = client.post("/api/recommend")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], "POST method not supported, please use GET")

        response = client.get("/api/recommend?number=10&page=0")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], USER_NAME_NONE)

    def test_extract_keyword(self):
        user = User.objects.filter(name="test").first()
        keyword_list = extract_keywords("[][][]蚂蚁集团重新上市或被推迟半年, 新疆新增新冠肺炎确诊病例2例", user, topk=5)
        self.assertEqual(len(keyword_list), 5)


class UserInfoTest(TestCase):
    def setUp(self):
        User.objects.create(name="test", pwhash="123456", mail="xxxx@qq.com", phone_number="123****4567")

    def test_user_info(self):
        client = Client()
        response = client.get("/api/user?username=test")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(response_json["mail"], "xxxx@qq.com")
        self.assertEqual(response_json["phone"], "123****4567")

        response = client.get("/api/user")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)
        self.assertEqual(response_json["data"], USER_NAME_NONE)
