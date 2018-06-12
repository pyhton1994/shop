# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from User.exceptions import *

# Create your models here.
class User(models.Model):
    account=models.EmailField(unique=True)
    password=models.CharField(max_length=100)

    # 只有序列化的时候使用到（隐藏部分字段）
    def __getstate__(self):
        print self.__dict__
        d = self.__dict__.copy()
        del d['password']
        return d



    @classmethod
    def register(cls,account,password,*args,**kwargs):
        print account,password,args,kwargs
        if cls.objects.filter(account=account).count()==1:
            raise UserExistException('账号已存在')

        user= cls.objects.create(account=account,password=password)
        return user


    @classmethod
    def is_exist(cls,email):
        return cls.objects.filter(account=email).count()==1

    @classmethod
    def login(cls, account, password, time, *args, **kwargs):
        if cls.objects.filter(account=account, password=password).count() == 0:
            raise UserNotExistException('当前账户不存在！')
        else:
            import time as t
            current = t.time() * 1000
            time = int(time)
            start = current - 1000 * 60 * 10
            if not (time > start and time < current):
                raise Exception('时间不对！')

            return cls.objects.get(account=account, password=password)
# 收货地址实体类
class Address(models.Model):
    uname = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    #是否是默认收货地址
    isdefault=models.BooleanField(default=False)