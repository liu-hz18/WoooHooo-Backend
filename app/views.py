""" app/views.py """
import json
from random import randint
import jieba
from django.http.response import JsonResponse
from django.shortcuts import HttpResponse

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
                "class": news type,
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
            'keywords': keywords
        })
    if request.method == "GET":
        keywords = []
        page = int(request.GET.get('page', default=0))
        number = int(request.GET.get('number', default=10))
        query = request.GET.get('query', default="")
        keywords = jieba.lcut_for_search(query)
        print(page, number, query, keywords)
        if page < 0 or number > 100 or query == "":       
            return gen_bad_response(400, [], keywords)
        newslist = [{
            'uid': i,
            'link': "https://www.baidu.com",
            'title': f" This is a random news {query} {i+page*number} "  * 10,
            'content': "这是新闻内容，" * 20,
            'imgurl': "http://inews.gtimg.com/newsapp_ls/0/12576682689_640330/0" if randint(0, 1) else "",
            'source': "xinhua net",
            'time': "2020.1.1",
        } for i in range(number)]
        return JsonResponse({
            'code': 200,
            'data': newslist,
            'keywords': keywords,
        })
    elif request.method == "POST":
        jsonObj = json.loads(request.body.decode())
        page = int(jsonObj.get('page'))
        number = int(jsonObj.get('number'))
        news_type = jsonObj.get('newstype')
        print(page, number, news_type)
        if page is None or number is None or news_type is None or page < 0 or number > 100 or news_type == "":
            return gen_bad_response(400, [], [news_type])
        newslist = [{
            'uid': i,
            'link': "https://www.baidu.com",
            'title': f" This is a random news {news_type}{i+page*number}"  * 10,
            'content': f"这是新闻内容，{news_type}" * 20,
            'imgurl': "http://inews.gtimg.com/newsapp_ls/0/12576682689_640330/0" if randint(0, 1) else "",
            'source': "xinhua net",
            'time': "2020.1.1",
        } for i in range(number)]
        return JsonResponse({
            'code': 200,
            'data': newslist,
            'keywords': [news_type],
        })
