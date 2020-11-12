# coding:utf-8
import re
import random
import json
import requests
import pymongo
from bs4 import BeautifulSoup as bs

host = "49.233.52.61"
database_name = "NewsCopy"
db_port = 30001
colomn_name = "news"
http_prefix = "http:"
lucene_url = f"{http_prefix}//{host}:30002/queryNews"
type_map = {
    "热点": "hot",
    "国内": "politics",
    "文化": "history",  # "cul"
    "社会": "social",
    "国际": "chuguo",
    "军事": "mil",
    "财经": "finance",
    "娱乐": "ent",
    "体育": "sports", 
    "科技": "science", # "tech"
    "游戏": "game",
}
pc_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"
]
referer = lambda url: re.search(r"^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)", url).group()

def decode(news):
    if news["top_img"] and len(news["top_img"]) > 5:
        img_url = http_prefix + news["top_img"].lstrip("http:")
    else:
        imgs = news["imageurl"]
        if isinstance(imgs, str):
            imgs = json.loads(imgs)
        if len(imgs) > 0:
            img_url = http_prefix + imgs[0].lstrip("http:")
        else:
            img_url = ""
    return {
        "uid": str(news['_id']),
        "link": news["url"],
        "title": news["title"],
        "content": news["content"][:300],
        "imgurl": img_url,
        "source": news["source"],
        "time": news["publish_time"]
    }

def io_db(news_col, query, ret_field, begin, number):
    result, total = [], news_col.estimated_document_count()
    for x in news_col.find(query, ret_field).sort([("publish_time", pymongo.DESCENDING)]).skip(begin).limit(number):  # 注意限制个数，不然数据量可能极大
        result.append(decode(x))
    return total, result

def fetch_typed_news(news_type, number, page):
    total = 0
    result = []
    newsdb_client = pymongo.MongoClient(f"mongodb://{host}:{db_port}/")
    newsdb = newsdb_client[database_name]
    news_col = newsdb[type_map[news_type]]
    print(news_col)
    query = {}
    ret_field = { # 为1的字段会返回
        '_id': 1,
        "title": 1,
        "publish_time": 1,
        "source": 1,
        "imageurl": 1,
        "url": 1,
        'content': 1,
        "top_img": 1,
    }
    print(total, page, number)
    total, result = io_db(news_col, query, ret_field, page*number, number)
    newsdb_client.close()
    print("**** exit from DB ****")
    return total, result


def fetch_search_result(query, number, page, relation=0):
    result = []
    #向java端发送检索请求
    params = {
        "name": query,
        "page": page,
        "number": number,
        "relation": relation
    }
    response = requests.get(url=lucene_url, params=params)
    search_result_json = json.loads(response.text)
    total = search_result_json["total"]
    newslist = search_result_json["data"]
    # print(newslist)
    for x in newslist:
        result.append(decode(x))
    return total, result


def fetch_hotlist():
    result = []
    newsdb_client = pymongo.MongoClient(f"mongodb://{host}:{db_port}/")
    newsdb = newsdb_client[database_name]
    news_col = newsdb["hot_click"]
    print(news_col)
    ret_field = {'_id': 1, "rank": 1, "title": 1, "url": 1, "publish_time": 1}
    for x in news_col.find({}, ret_field).sort([("rank", pymongo.ASCENDING)]).limit(10):  # 注意限制个数，不然数据量可能极大
        result.append({"uid": str(x["_id"]), "title": x["title"], "link": x["url"], "time": x["publish_time"]})
    news_col = newsdb["hot_comment"]
    ret_field = {'_id': 1, "rank": 1, "title": 1, "url": 1, "publish_time": 1}
    for x in news_col.find({}, ret_field).sort([("rank", pymongo.ASCENDING)]).limit(10):
        result.append({"uid": str(x["_id"]), "title": x["title"], "link": x["url"], "time": x["publish_time"]})
    newsdb_client.close()
    print("**** exit from server ****")
    return result


def fetch_hot_search():
    result = []
    newsdb_client = pymongo.MongoClient(f"mongodb://{host}:{db_port}/")
    newsdb = newsdb_client[database_name]
    news_col = newsdb["hot_search"]
    print(news_col)
    ret_field = {'_id': 1, "title": 1, "value": 1}
    for x in news_col.find({}, ret_field).limit(10):  # 注意限制个数，不然数据量可能极大
        result.append({"uid": str(x["_id"]), "title": x["title"], "value": x["value"]})
    newsdb_client.close()
    print("**** exit from server ****")
    return result


def get_related_search(content):
    base_url = f"https://www.sogou.com/web?query={content}"
    headers = {
        "User-Agent":random.choice(pc_agent),
        'Referer': referer(base_url),
        'DNT': "1",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()
    response.encoding = 'utf-8'
    soup = bs(response.text, "html.parser")
    title = soup.select("#hint_container > tr > td > p > a")
    print(title, headers["User-Agent"])
    title_list = []
    for index in title:
        title_list.append(index.text)
    return title_list
