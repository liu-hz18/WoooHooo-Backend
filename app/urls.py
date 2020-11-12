"""urls """
from django.urls import path

from . import views

# borad应用的路由配置
urlpatterns = [
    path('index', views.index, name='index'),
    path('search', views.search, name='search'),
    path('hot', views.hot, name='hot'),
    path('hotsearch', views.hot_search, name="hotsearch"),
]
