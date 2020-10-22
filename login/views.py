import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError

from .models import User
from .utils import send_validation_email


def gen_response(code: int, data: str):
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def login(request):
    #Get用来验证登录
    if request.method == 'GET':
        username = ""
        password = ""
        print(request.GET.items())
        username = request.GET.get('username', default="")
        password = request.GET.get('userpass', default="")
        print("username: ", username, "password: ", password)
        #如果前端没传过来用户名和密码
<<<<<<< HEAD
        if password == "" or username == "":
            return gen_response(405, "there is no username or password or None")
=======
        if not password or not username:
            return gen_response(400, "there is no username or password")
>>>>>>> f770fff (update:change the reponse information if something is wrong)
        #利用用户名获取用户
        user = User.objects.filter(name=username).first()
        #若用户不存在
        if not user:
            return gen_response(400, "username Error")
        #检查密码
        if user.password == password:
            return gen_response(200, "successful user validation")
        return gen_response(401, "password Error")
    #用Post来完成注册
    elif request.method == 'POST':
        print(request.body.decode())
        try:
            user = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return gen_response(403 , "the data is not json")
        username = user.get('username')
        password = user.get('userpass')
        if not username or not password:
            return gen_response(400, "there is no username or password")
<<<<<<< HEAD
        # 检查用户是否已经存在
=======
        #检查用户是否已经存在
>>>>>>> f770fff (update:change the reponse information if something is wrong)
        user = User.objects.filter(name=username).first()
        if user:
            return gen_response(401, "user is already existed")
        user = User(name=username,password=password)
        print(user)
        try:
            user.full_clean() #检查用户名的有效性
            user.save() # 存入数据库
            return gen_response(200, "user was set successfully")
        except ValidationError as e:
            return gen_response(400, "length Error of user: {}".format(e))
    else:
        return gen_response(400, "Unknown Error")


def validate(request):
    if request.method == "POST":
        print("mail:", request.body.decode())
        try:
            mail_json = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return gen_response(403 , "the data is not json")
        username = mail_json.get('username')
        mail_addr = mail_json.get("mail")
        if not mail_addr or not username or username == "":
            return gen_response(400, "mail address or username error")
        key = send_validation_email(username, mail_addr)
        print("validation key: ", key)
        if key < 0:
            return gen_response(400, "mail address format error")
        return gen_response(200, key)
    else:
        return gen_response(400, "GET method not supported, please use POST")
