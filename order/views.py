# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views import View
# Create your views here.
class OrderView(View):
    def get(self,request):
        import jsonpickle
        # 判断当前用户是否登录
        if not request.session.get('user'):

            return HttpResponseRedirect('/user/login/?redirect=order&cartitems=' + request.GET.get('cartitems'))
        else:

            # 将购物项反序列化成[{k:v}{k:v}]形式列表对象

            # [{'goodsid':'','sizeid':'','colorid':''},{},{}]
            raw_cartitems = jsonpickle.loads('[' + request.GET.get('cartitems') + ']')

            # 目前还没有创建订单
            # 将购物项存放至session对象中

            request.session['raw_cartitems'] = raw_cartitems
            return HttpResponseRedirect('/order/order.html')

from cart.cartmanager import *

class OrderListView(View):
    def get(self,request):

        #获取当前用户下的购物项
        cart_manager = getCartManger(request)

        cartitems = [cart_manager.get_cartitems(**item) for item in request.session.get('raw_cartitems',[])]


        #获取当前用户下的默认收货地址
        address = request.session.get('user').address_set.get(isdefault=True)


        #计算结算总金额
        totalprice = 0
        for cartitem in cartitems:
            totalprice+=cartitem.total_price()

        return render(request,'order.html',{'cartitems':cartitems,'address':address,'totalprice':totalprice})
