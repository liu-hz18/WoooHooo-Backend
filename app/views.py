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
        page = int(request.GET.get('page', default=0))
        number = int(request.GET.get('number', default=10))
        query = request.GET.get('query', default="")
        keywords = sorted(jieba.lcut_for_search(query), key=len, reverse=True)
        print(page, number, query, keywords)
        if page < 0 or number > 100:       
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
        }, status=200)
