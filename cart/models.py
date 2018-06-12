# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from newgoods.models import Goods,Color,Size
from User.models import User

class CartItem(models.Model):
    goodsid = models.IntegerField()
    colorid = models.IntegerField()
    sizeid = models.IntegerField()
    count = models.PositiveIntegerField()#正整数
    user = models.ForeignKey(User)
    isdelete = models.BooleanField(default=False)

    class Meta:
        unique_together=['goodsid','colorid','sizeid']

    def goods(self):
        return Goods.objects.get(id=self.goodsid)

    def color(self):
        return Color.objects.get(id=self.colorid)

    def size(self):
        return Size.objects.get(id=self.sizeid)

    def total_price(self):
        return int(str(self.count))*float(str(self.goods().price))