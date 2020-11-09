# coding:utf-8
import json
import requests
import pymongo
from bs4 import BeautifulSoup as bs

host = "49.233.52.61"
database_name = "NewsCopy"
db_port = 30001
colomn_name = "news"
http_prefix = "http:"
lucene_url = "http://49.233.52.61:30002/queryNews"
type_map = {
    "热点": "news",
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


def fetch_search_result(query, number, page, relation=1):
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
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    base_url = f"https://www.sogou.com/web?query={content}"
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()
    response.encoding = 'utf-8'
    soup = bs(response.text, "html.parser")
    title = soup.select("#hint_container > tr > td > p > a")
    title_list = []
    for index in title:
        title_list.append(index.text.split()[0])
    return title_list
