""" app/views.py """
import json
import jieba
from django.http.response import JsonResponse
from django.shortcuts import HttpResponse

from .newsapi import fetch_typed_news, fetch_search_result
# Create your views here.


def index(request):
    """function index"""
    return HttpResponse("Hello world")

def search(request):
    """
    backend search api to frontend
    request api: 
        post:
            {
                "newstype": news type,
                "page": page offset,
                "number": return news number
            }
            return {
                data: newslist
            }
        get:
           {
               "query": query string,
               "page": page offset,
               "number": return number news
           } 
           return {
               data: newslist,
               total: total result,
               keywords: use `jieba` to split query
           }
    """
    def gen_bad_response(code: int, data: list, keywords: list):
        return JsonResponse({
            'code': code,
            'data': data,
            'keywords': keywords,
            'total': 0,
        }, status=code)
    if request.method == "GET":
        keywords = []
<<<<<<< HEAD
        page = int(request.GET.get('page', default=0))
        number = int(request.GET.get('number', default=10))
        query = request.GET.get('query', default="")
        keywords = sorted(jieba.lcut_for_search(query), key=len, reverse=True)
=======
        page = 0
        number = 0
        query = ""
        print(request.body.decode())
        page = int(request.GET.get('page', default=0))
        number = int(request.GET.get('number', default=10))
        query = request.GET.get('query', default="")
<<<<<<< HEAD
<<<<<<< HEAD
        keywords = jieba.lcut_for_search(query)
>>>>>>> 29c9924 (change: move useless / url and update GET api)
=======
        keywords = sorted(jieba.lcut_for_search(query), key = lambda word:len(word), reverse=True)
>>>>>>> 408b019 (upd: keyword cut will be sorted by length)
=======
        keywords = sorted(jieba.lcut_for_search(query), key=len, reverse=True)
>>>>>>> 4b9f76e (upd: keyword cut will be sorted by length)
        print(page, number, query, keywords)
        if page < 0 or number > 100 or query == "":       
            return gen_bad_response(400, [], keywords)
        try:
            total, newslist = fetch_search_result(query, number, page)
        except Exception as e:
            total, newslist = 0, []
            print("error in search():", e)
        return JsonResponse({
            'code': 200,
            'data': newslist,
            'keywords': keywords,
            'total': total
        }, status=200)
    elif request.method == "POST":
        print(request.body.decode())
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b3f5e91 (upd: provide keywords field in news type return)
        json_obj = json.loads(request.body.decode())
        page = json_obj.get('page')
        number = json_obj.get('number')
        news_type = json_obj.get('newstype')
<<<<<<< HEAD
=======
        jsonObj = json.loads(request.body.decode())
        page = jsonObj.get('page')
        number = jsonObj.get('number')
        news_type = jsonObj.get('newstype')
>>>>>>> 4b9f76e (upd: keyword cut will be sorted by length)
=======
>>>>>>> b3f5e91 (upd: provide keywords field in news type return)
        print(page, number, news_type)
        if page is None or number is None or news_type is None or page < 0 or number > 100:
            return gen_bad_response(400, [], [news_type])
        page, number = int(page), int(number)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        total, newslist = fetch_typed_news(news_type, number, page)
=======
=======
        total = 1024
>>>>>>> ee3216d (upd: add 	otal param in news type api)
        newslist = [{
            'uid': i,
            'link': "https://www.baidu.com",
            'title': f" This is a random news from backend {news_type}{i+page*number}"  * 10,
            'content': f"这是新闻内容，{news_type}" * 20,
            'imgurl': "http://inews.gtimg.com/newsapp_ls/0/12576682689_640330/0" if randint(0, 1) else "",
            'source': "xinhua net",
            'time': "2020.1.1",
        } for i in range(number)]
>>>>>>> 4b9f76e (upd: keyword cut will be sorted by length)
=======
        total, newslist = fetch_typed_news(news_type, number, page)
>>>>>>> f48baab (add: news type fetch api from newsdb)
        return JsonResponse({
            'code': 200,
            'data': newslist,
<<<<<<< HEAD
<<<<<<< HEAD
            'keywords': [],
            'total': total,
        }, status=200)
=======
            'keywords': [news_type],
=======
            'keywords': [],
>>>>>>> b3f5e91 (upd: provide keywords field in news type return)
            'total': total,
        })
>>>>>>> ee3216d (upd: add 	otal param in news type api)
