import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError

from .models import User, BrowseHistory, SearchHistory
from .utils import send_validation_email

NOT_JSON_INFO = "the data is not json"

def gen_response(code: int, data: str):
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def login(request):
    #Get用来验证登录
    if request.method == 'GET':
        print(request.GET.items())
        username = request.GET.get('username', default="")
        password = request.GET.get('userpass', default="")
        print("username: ", username, "password: ", password)
        #如果前端没传过来用户名和密码
        if password == "" or username == "":
            return gen_response(400, "there is no username or password or None")
        #利用用户名获取用户
        user = User.objects.filter(name=username).first()
        #若用户不存在
        if not user:
            return gen_response(400, "username Error")
        #检查密码
        if user.password == password:
            return gen_response(200, "successful user validation")
        return gen_response(400, "password Error")
    #用Post来完成注册
    elif request.method == 'POST':
        print(request.body.decode())
        try:
            user = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return gen_response(400, NOT_JSON_INFO)
        username = user.get('username')
        password = user.get('userpass')
        if not username or not password:
            return gen_response(400, "there is no username or password")
        # 检查用户是否已经存在
        user = User.objects.filter(name=username).first()
        if user:
            return gen_response(400, "user is already existed")
        user = User(name=username, password=password)
        print(user)
        try:
            user.full_clean() #检查用户名的有效性
            user.save() # 存入数据库
            return gen_response(200, "user was set successfully")
        except ValidationError as e:
            return gen_response(400, "DB Error of user: {}".format(e))


def validate(request):
    if request.method == "POST":
        print("mail:", request.body.decode())
        try:
            mail_json = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return gen_response(400, NOT_JSON_INFO)
        username = mail_json.get('username')
        mail_addr = mail_json.get("mail")
        if not mail_addr or not username or username == "":
            return gen_response(400, "mail address or username error")
        key = send_validation_email(username, mail_addr)
        print("validation key: ", key)
        if key == "-1":
            return gen_response(400, "mail address format error")
        return gen_response(200, key)
    else:
        return gen_response(400, "GET method not supported, please use POST")


def browsehis(request):
    if request.method == "POST": # add browsing info into DB
        print("browsing post:", request.body.decode())
        try:
            json_data = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return gen_response(400, NOT_JSON_INFO)
        name = json_data.get('username')
        news = json_data.get("newsinfo")
        if not name or not news or name == "":
            return gen_response(400, "username or newsinfo is None!")
        if isinstance(news, str):
            news = json.loads(news)
        user = User.objects.filter(name=name).first()
        if not user:
            return gen_response(400, "username don't exist.")
        print(user, news, name)
        browsing_history = BrowseHistory(
            user=user, uid=news.get("uid"), title=news.get("title"), imgurl=news.get("imgurl"), 
            content=news.get("content"), link=news.get("link"), source=news.get("source"), time=news.get("time")
        )
        print(browsing_history)
        try:
            browsing_history.full_clean()
            browsing_history.save()
        except ValidationError as _:
            return gen_response(400, 'news info length is too long')
        return gen_response(200, "browsing history logged successfully")
    elif request.method == "GET":
        name = request.GET.get('username', default="")
        if not name or name == "":
            return gen_response(400, "user name should not be None or blank")
        user = User.objects.filter(name=name).first()
        result = []
        browse_his = user.browsehistory_set.all()
        total = browse_his.count()
        for history in browse_his:
            result.append({
                "uid": history.uid,
                "title": history.title,
                "imgurl": history.imgurl,
                "content": history.content,
                "link": history.link,
                "source": history.source,
                "time": history.time,
                #"logtime": history.browse_time,
            })
        return JsonResponse({
            "code": 200,
            "data": result,
            "total": total,
        })


def searchhis(request):
    if request.method == "POST": # add search info into DB
        print("searching post:", request.body.decode())
        try:
            json_data = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return gen_response(400 , NOT_JSON_INFO)
        name = json_data.get('username')
        content = json_data.get("data")
        if name is None or content is None or name == "":
            return gen_response(400, "username or search content is None!")
        user = User.objects.filter(name=name).first()
        if not user:
            return gen_response(400, "username don't exist.")
        print(name, content)
        searching_history = SearchHistory(user=user, content=content)
        try:
            searching_history.full_clean()
            searching_history.save()
        except ValidationError as _:
            return gen_response(400, 'search content length is too long')
        return gen_response(200, "searching history logged successfully")
    elif request.method == "GET":
        name = request.GET.get('username', default="")
        if not name or name == "":
            return gen_response(400, "user name should not be None or blank")
        user = User.objects.filter(name=name).first()
        result = []
        search_his = user.searchhistory_set.all()
        total = search_his.count()
        for history in search_his:
            result.append(history.content)
        return JsonResponse({
            "code": 200,
            "data": result,
            "total": total,
        })
