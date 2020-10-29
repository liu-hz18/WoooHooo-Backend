import pymongo
from sshtunnel import SSHTunnelForwarder

host = "49.233.52.61"
port = 22
# better changed to SSH
username = "ubuntu"
password = "48*~VbNY93Aq"
database_name = "StaticNews"
db_port = 27017
local_port = 27018 # should be different from `db_port`
colomn_name = "news"

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

def fetch_typed_news(news_type, number, page):
    total = 0
    result = []
    with SSHTunnelForwarder(
        ssh_address_or_host=(host, port),  # 远程主机ip, port
        ssh_username=username,  # ssh用户名密码
        ssh_password=password,
        remote_bind_address=('127.0.0.1', db_port),     # 远程服务ip, port
        local_bind_address=('localhost', local_port)    # 转发到本地服务ip, port
    ) as server:
        newsdb_client = pymongo.MongoClient(f"mongodb://localhost:{local_port}/")
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
        }
        total = news_col.count()
        for x in news_col.find(query, ret_field).skip(page*number).limit(number):  # 注意限制个数，不然数据量可能极大
            if len(x["imageurl"]) > 0:
                img_url = "http://" + x["imageurl"][0].strip('//')
            else:
                img_url = ""
            result.append({
                "uid": str(x['_id']),
                "link": x["url"],
                "title": x["title"],
                "content": x["content"][:300],
                "imgurl": img_url,
                "source": x["source"],
                "time": x["publish_time"]
            })
        newsdb_client.close()
        print("**** exit from server ****")
    return total, result


def fetch_search_result(query, number, page):
    total = 0
    result = []
    with SSHTunnelForwarder(
        ssh_address_or_host=(host, port),  # 远程主机ip, port
        ssh_username=username,  # ssh用户名密码
        ssh_password=password,
        remote_bind_address=('127.0.0.1', db_port),     # 远程服务ip, port
        local_bind_address=('localhost', local_port)    # 转发到本地服务ip, port
    ) as server:
        newsdb_client = pymongo.MongoClient(f"mongodb://localhost:{local_port}/")
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
        }
        total = news_col.count()
        for x in news_col.find(query, ret_field).skip(page*number).limit(number):  # 注意限制个数，不然数据量可能极大
            result.append({
                "uid": str(x['_id']),
                "link": x["url"],
                "title": x["title"],
                "content": x["content"][:200],
                "imgurl": x["imageurl"][0],
                "source": x["source"],
                "time": x["publish_time"]
            })
        newsdb_client.close()
        print("**** exit from server ****")
    return total, result

