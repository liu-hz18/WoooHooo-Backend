from django.db import models
from django.forms import ModelForm

class User(models.Model):
    #用户名
    name = models.CharField(unique=True, max_length=200)
    #密码
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name