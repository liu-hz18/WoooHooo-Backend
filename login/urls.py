from django.urls import path

from . import views

# login应用的路由配置
urlpatterns = [
    path('login', views.login, name='login'),
    path('validate', views.validate, name='validate'),
    path('browsehis', views.browsehis, name='browsehis'),
    path('searchhis', views.searchhis, name='searchhis'),
    path('recommend', views.recommend, name='recommend'),
    path('user', views.user, name="user"),
    path('update', views.update, name="update"),
]
