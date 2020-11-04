from django.db import models
from django.forms import ModelForm

class User(models.Model):
    name = models.CharField(unique=True, max_length=100) # 用户名
    pwhash = models.CharField(max_length=200) # 密码

    def __str__(self):
        return self.name


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(unique=True, max_length=100)


class BrowseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 外键指向User的主键, 跟随外键删除
    uid = models.CharField(unique=True, max_length=50)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=350)
    imgurl = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    source = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    browse_time = models.DateTimeField(auto_now_add=True)


class KeyWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 外键指向User的主键, 跟随外键删除
    keyword = models.CharField(unique=True, max_length=30)
