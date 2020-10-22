import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from .models import User


def login(request):
    def gen_response(code: int, data: str):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    #Get用来验证登录
    if request.method == 'GET':
        user = json.loads(request.body.decode())
        print(user)
        username = user.get('username')
        password = user.get('userpass')
        #如果前端没传过来用户名和密码
        if not password or not username:
            return gen_response(400, "there is no username or password")
        #利用用户名获取用户
        user = User.objects.filter(name=username).first()
        #若用户不存在
        if not user:
            return gen_response(400, "username Error")
        #检查密码
        if user.password==password:
            return gen_response(200, "successful user validation")
        return gen_response(401, "password Error")
    #用Post来完成注册
    elif request.method == 'POST':
        user = json.loads(request.body.decode())
        print(user)
        username = user.get('username')
        password = user.get('userpass')
        if not username or not password:
            return gen_response(400, "there is no username or password")
        #检查用户是否已经存在
        user = User.objects.filter(name=username).first()
        if user:
            return gen_response(401, "user is already existed")
        user = User(name=username,password=password)
        print(user)
        try:
            #检查用户名的有效性
            user.full_clean()
            # 存入数据库
            user.save()
            return gen_response(200, "user was set successfully")
        except ValidationError as e:
            return gen_response(400, "length Error of user: {}".format(e))

