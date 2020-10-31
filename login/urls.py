from django.urls import path

from . import views

# login应用的路由配置
urlpatterns = [
    path('login', views.login, name='login'),
    path('validate', views.validate, name='validate'),
]
