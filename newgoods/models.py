# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=20,unique=True)

    def __unicode__(self):
        return u'%s'%self.name

    class Meta:
        verbose_name_plural='类别'
        ordering=['id']

class Goods(models.Model):
    name=models.CharField(max_length=100,verbose_name='商品名称')
    desc = models.CharField(max_length=100,verbose_name='商品描述')
    price=models.DecimalField(max_digits=5,decimal_places=2,verbose_name='现价')
    oldprice=models.DecimalField(max_digits=5,decimal_places=2,verbose_name='原价')
    category=models.ForeignKey(Category)

    def __unicode__(self):
        return u'%s'%self.name


    class Meta:
        verbose_name_plural='商品'
        ordering=['id']

    def getImg(self):
        return self.inventory_set.first().color.value

    def getColors(self):
        colors = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in colors:
                colors.append(color)
        return colors

    def getSizes(self):
        sizes =[]

        for inventory in self.inventory_set.all():
            size = inventory.size
            if size not in sizes:
                sizes.append(size)

        return sizes


    def getDetails(self):
        import collections
        datas = collections.OrderedDict()


        for detail in self.goodsdetailsitem_set.all():
            dname = detail.name()
            if dname not in datas:
                datas[detail.name()]=[detail.values]
            else:
                datas[detail.name()].append(detail.values)


        return datas


class Color(models.Model):
    name=models.CharField(max_length=20)
    value=models.ImageField(upload_to='media/color/')

    def __unicode__(self):
        return u'%s'%self.name


    class Meta:
        verbose_name_plural='颜色'
        ordering=['id']

class Size(models.Model):
    name=models.CharField(max_length=20)
    value=models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s'%self.name


    class Meta:
        verbose_name_plural='尺寸'
        ordering=['id']

class GoodsDetails(models.Model):

    name=models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s'%self.name


    class Meta:
        verbose_name_plural='详情'
        ordering=['id']

class GoodsDetailsItem(models.Model):
    goods = models.ForeignKey(Goods)
    goodsdetails=models.ForeignKey(GoodsDetails,verbose_name='详情')
    values=models.ImageField(upload_to='media/',verbose_name='图片')

    def name(self):
        return self.goodsdetails.name


    def __unicode__(self):
        return u'%s'%self.values


    class Meta:
        verbose_name_plural = '详细条目'
        ordering = ['id']
#库存表
class Inventory(models.Model):
    color = models.ForeignKey(Color)
    size = models.ForeignKey(Size)
    goods = models.ForeignKey(Goods)
    count=models.IntegerField(default=100)

    def __unicode__(self):
        return u'%s'%self.count


    class Meta:
        verbose_name_plural='库存'
        ordering=['id']
