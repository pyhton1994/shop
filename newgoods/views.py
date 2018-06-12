# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views import View
# Create your views here.

from .models import *
from utils.pageutil import *

class IndexView(View):
    #查询所有的类别
    categorys = Category.objects.all()
    #查询第一个类别的id
    current_categoryid = Category.objects.first().id

    def get(self, request, categoryid=None, pagenum=1):



        if categoryid == None:
            current_cid = self.current_categoryid
        else:
            current_cid = categoryid
        pages, goods = get_objects_page(Goods.objects.filter(category_id=current_cid), pagenum)

        # goods = Goods.objects.filter(category_id=current_cid)
        return render(request, 'index.html',
                      {'categorys': self.categorys, 'current_cid': int(current_cid), 'goods': goods, 'pages': pages})


# 利用装饰器实现推荐商品功能
def wrapper_recommend_goods_cookie(func):
    def _wrapper(detailView,request,goodsid,*args,**kwargs):

        raw_commend_goods = request.COOKIES.get('recommend_goods','')

        commend_goods = [item for item in raw_commend_goods.split() if item.strip()]

        print type(commend_goods)

        # 自定义算法获取前四个推荐商品
        recommend_goods = [Goods.objects.get(id=c_good) for c_good in commend_goods if c_good!=goodsid and Goods.objects.get(id=goodsid).category_id==Goods.objects.get(id=c_good).category_id][:4]
        print type(recommend_goods)
        #调用func函数获取响应对象
        response = func(detailView,request,goodsid,recommend_goods,*args,**kwargs)

        # 判断商品id是否在commend_goods列表中存在
        # 最新浏览过的商品在最前面显示
        if goodsid not in commend_goods:
            commend_goods.append(goodsid)
        else:
            commend_goods.remove(goodsid)
            commend_goods.insert(0,goodsid)

        #将推荐商品列表存放至cookie中（单位秒）
        response.set_cookie('recommend_goods',' '.join(commend_goods),max_age=60*60*24*3)

        return response
    return _wrapper




class DetailView(View):
    @wrapper_recommend_goods_cookie
    def get(self,request,goodsid,recommend_goods=[]):
        goodsid = int(goodsid)
        print(goodsid)
        goods = Goods.objects.get(id=goodsid)

        return render(request,'detail.html',{'goods':goods,'recommend_goods':recommend_goods})
