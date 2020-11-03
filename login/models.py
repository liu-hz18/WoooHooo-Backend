from django.db import models
from django.forms import ModelForm

class User(models.Model):
    name = models.CharField(unique=True, max_length=200) # 用户名
    password = models.CharField(max_length=200) # 密码

    def __str__(self):
        return self.name
