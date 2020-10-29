import requests
import demjson
from bs4 import BeautifulSoup
import json
from Scratchtest import *
import pymongo
import time

def loadTencentNews():
    #各种频道
    channels=['24hours','video','milite','cul','nstock','comic','house','emotion','digi','astro','health',
             'visit','baby','pet','history','politics','zfw','football','newssh','rushidao','edu','licai',
             'sports','life','kepu','ent','antip','bj','world','tech','finance','auto','fashion','games']
    baseurls = " https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://news.qq.com',
        'referer': 'https://news.qq.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    }
    params = {
        'sub_srv_id': 'video',
        'srv_id': 'pc',
        'offset': 0,
        'limit': 10,
        'strategy': 1,
        'ext': "{\"pool\":[\"top\"], \"is_filter\":10, \"check_type\":true}",
    }
    urls=[]
    for index in channels:
        try:
            params['sub_srv_id']=index
            response = requests.get(baseurls, params=params, headers=headers)
            news_list = demjson.decode(response.content)["data"]["list"]
            for news in news_list:
                urls.append(news['url'])
        except:
            continue
    return list(set(urls))

#处理热点新闻列表
def handleNewslist(urls):
    updatedNews=[]
    for url in urls:
        try:
            news=loadWithTime(url)
            updatedNews.append(news)
        except:
            continue
    return updatedNews



if __name__ == "__main__":
    myclient = pymongo.MongoClient("mongodb://localhost/")
    mydb = myclient["DynamicNews"]
    newsSet=mydb["news"]
    totalurls=[]
    while True:
        updatedurls=loadTencentNews()
        for url in updatedurls:
            if url in totalurls:
                updatedurls.remove(url)
            else:
                totalurls.append(url)
        if len(updatedurls)!=0:
            updatedNews=handleNewslist(updatedurls)
            if len(updatedNews)!=0:
                x = newsSet.insert_many(updatedNews)
                print(len(updatedNews))
        print("epoch end")
        time.sleep(10)



