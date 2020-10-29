""" app/views.py """
import json
import http.client 
from random import randint
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
        })
    if request.method == "GET":
        keywords = []
        page = 0
        number = 0
        query = ""
        for k,v in request.GET.items():
            print(k)
            print(v)
            if k == "page":
                page = v
            elif k == "number":
                number = v
            elif k == "query":
                query = v
        keywords = sorted(jieba.lcut_for_search(query), key=len, reverse=True)
        print(page, number, query, keywords)
        if page < 0 or number > 100 or query == "":       
            return gen_bad_response(400, [], keywords)
        total = 1000
        #向java端发送检索请求
        newslist = None
        try:
            httpClient = http.client.HTTPConnection('https://wooohooo-indexquery-wooohooo.app.secoder.net/', 80, timeout=30)
            httpClient.request('GET', f'/queryNews?name={query}&page={page}&number={number}')
            #response是HTTPResponse对象
            response = httpClient.getresponse()
            print(response.read().decode())
            newslist = response.read().decode()
        except ConnectionRefusedError as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()
        '''
        newslist = [{
            'uid': i,
            'link': "https://www.baidu.com",
            'title': f" This is a random news from backend {query} {i+page*number} "  * 10,
            'content': "这是新闻内容，" * 20,
            'imgurl': "http://inews.gtimg.com/newsapp_ls/0/12576682689_640330/0" if randint(0, 1) else "",
            'source': "xinhua net",
            'time': "2020.1.1",
        } for i in range(number)]
        '''
        return JsonResponse({
            'code': 200,
            'data': newslist,
            'keywords': keywords,
            'total': total
        })
    elif request.method == "POST":
        print(request.body.decode())
        json_obj = json.loads(request.body.decode())
        page = json_obj.get('page')
        number = json_obj.get('number')
        news_type = json_obj.get('newstype')
        print(page, number, news_type)
        if page is None or number is None or news_type is None or page < 0 or number > 100:
            return gen_bad_response(400, [], [news_type])
        page, number = int(page), int(number)
        total, newslist = fetch_typed_news(news_type, number, page)
        return JsonResponse({
            'code': 200,
            'data': newslist,
            'keywords': [],
            'total': total,
        })
