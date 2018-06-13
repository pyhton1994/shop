# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from cartmanager import *


# Create your views here.
class CartView(View):
    def post(self,request):
        # 显式的告诉会话对象被修改了。默认情况下只有session被创建或修改才会被存储到数据库中
        request.session.modified = True

        # 判断当前操作类型
        # 加入购物车操作
        if request.POST.get('type') == 'add':
            self.add(request)
            return HttpResponseRedirect('cart.html')



    def add(self,request):
        cart_manager = getCartManger(request)
        cart_manager.add(**request.POST.dict())


class CartListView(View):
    def get(self,request):
        # 查询购物车中的所有商品
        cartItems = getCartManger(request).queryAll()
        return render(request, 'cart.html', {'cartItems': cartItems})