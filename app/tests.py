"""test"""
import random
import json
import requests
from django.test import TestCase, Client

from .apps import AppLocalConfig
from .views import gen_bad_response
from .newsapi import decode, io_db

# Create your tests here.
class APITest(TestCase):
    """Main Test"""

    def check_news_json_ok(self, news):
        self.assertIn("uid", news)
        self.assertIn("link", news)
        self.assertIn("title", news)
        self.assertIn("imgurl", news)
        self.assertIn("time", news)
        self.assertIn("source", news)

    def test_index_page(self):
        client = Client()
        response = client.post("/api/index")
        self.assertEqual(response.content, b"Hello world")

    def test_search_api(self):
        number = random.randint(1, 30)
        page = random.randint(0, 10)
        client = Client()
        response = client.get(f"/api/search?page={page}&number={number}&query=新闻")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(len(response_json["data"]), number)
        self.check_news_json_ok(response_json["data"][0])
        page = -1
        response = client.get(f"/api/search?page={page}&number={number}&query=新闻")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 400)

    def test_typenews_api(self):
        number = 0
        page = 0
        client = Client()
        page = -1
        response = client.post("/api/search", data={"page": page, "number": number, "newstype": "热点"}, content_type="application/json")
        response_json = response.json()
        self.assertEqual(response_json["code"], 400)
        page = 0
        number = 100
        response = client.post("/api/search", data={"page": page, "number": number, "newstype": "国内"}, content_type="application/json")
        response_json = json.loads(response.content)
        self.assertEqual(response_json["code"], 200)
        self.assertEqual(len(response_json["data"]), 0)

    def test_app_config(self):
        self.assertEqual(AppLocalConfig.name, 'app')

    def test_gen_response(self):
        ret = json.loads(gen_bad_response(200, ['test'], ["新闻"]).content)
        self.assertEqual(ret["code"], 200)
        self.assertEqual(ret["data"], ['test'])
        self.assertEqual(ret["keywords"], ["新闻"])

    def test_decode(self):
        news_ret = decode({"_id": 0, "url": "", "content": "", "source": "", "publish_time": "", "title": "", "top_img": "//www.baidu.com", "imageurl": str(["//www.baidu.com", "//www.baidu.com"])})
        self.assertEqual(news_ret["imgurl"], "http://www.baidu.com")
        news_ret = decode({"_id": 0, "url": "", "content": "", "source": "", "publish_time": "", "title": "", "top_img": "//www.baidu.com", "imageurl": ["//www.baidu.com", "//www.baidu.com"]})
        self.assertEqual(news_ret["imgurl"], "http://www.baidu.com")
