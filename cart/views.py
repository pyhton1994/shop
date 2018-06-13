# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, JsonResponse
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

        # 移除购物车操作
        elif request.POST.get('type') == 'delete':
            self.delete(request)
            return JsonResponse({'result': True})

        # 增加购物车商品数量操作
        elif request.POST.get('type') == 'plus':
            self.plus(request)
            return JsonResponse({'result': True})

        # 减少购物车商品数量操作
        elif request.POST.get('type') == 'minus':
            self.minus(request)
            return JsonResponse({'result': True})




    def add(self,request):
        cart_manager = getCartManger(request)
        cart_manager.add(**request.POST.dict())

    def delete(self, request):
        cart_manager = getCartManger(request)
        cart_manager.delete(**request.POST.dict())

    def plus(self, request):
        cart_manager = getCartManger(request)

        cart_manager.update(step=1, **request.POST.dict())

    def minus(self, request):
        cart_manager = getCartManger(request)
        cart_manager.update(step=-1, **request.POST.dict())


class CartListView(View):
    def get(self,request):
        # 查询购物车中的所有商品
        cartItems = getCartManger(request).queryAll()
        return render(request, 'cart.html', {'cartItems': cartItems})