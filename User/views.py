# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.

from django.views import View

from cart.cartmanager import SessionCartManager
from .forms import *
from utils import code
from utils.loadaddr import *


class Register(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        datas = request.POST.dict()
        register_form= RegiterForm(datas)
        #当返回值为True说明表单校验成功
        if register_form.is_valid():
            user = User.register(**register_form.cleaned_data)
            request.session['user'] = user  #redis
            print request.session
            return HttpResponseRedirect('/user/usercenter/')
        else:
            return render(request,'register.html',{'errors':register_form.errors,'info':datas})

class UserCenterView(View):
    def get(self,request):
        return render(request, 'usercenter.html')


class Login(View):
    def get(self,request):
        # 获取登录成功后跳转参数
        redirect = request.GET.get('redirect', '')
        cartitems = request.GET.get('cartitems', [])
        return render(request, 'login.html', {'redirect': redirect, 'cartitems': cartitems})

    def post(self, request):
        try:
            # 验证是否登录成功
            user = User.login(**request.POST.dict())
            request.session['user'] = user

            # 将购物项信息存放至数据库
            SessionCartManager(request.session).migrateSession2DB()
            # 登录成功后页面进行相应的跳转

            if request.POST.get('redirect') == 'cart':
                return HttpResponseRedirect('/cart/cart.html')
            elif request.POST.get('redirect') == 'order':
                return HttpResponseRedirect('/order?cartitems=' + request.POST.get('cartitems'))

            return HttpResponseRedirect('/user/usercenter/')

        except UserNotExistException:
            # 没有登录成功就跳转至登录页面
            return render(request, 'login.html')

# 生成验证码
class Code(View):
    def get(self,request):
        img,str= code.gene_code()
        request.session['sessioncode']=str
        return HttpResponse(img,content_type='image/png')

# 校验验证码
class CheckCode(View):
    def get(self,request):
        code = request.GET.get('code',None)
        scode = request.session.get('sessioncode','-1')
        result = code == scode
        return JsonResponse({'checkFlag':result})
#退出登录操作
class Logout(View):

    def post(self,request):
        if 'user' in request.session:
            del request.session['user']
        return JsonResponse({'Flag':True})
#地址管理
html='''<div id='dizhi'><p>{name}</p><p>{phone}</p><p>{address}</p><p>{details}</p></div>'''
class UserAddressView(View):
    def get(self,request):
        #查询默认的省市区的信息
        provinces= get_provinces()
        citys,areas = get_citys_areas_by_provinceid('110000')

        return render(request,'address.html',{'provinces':provinces,'citys':citys,'areas':areas})

    def post(self, request):
        type = request.POST.get('type', '1')
        if type == '1':
            provinceId = request.POST.get('provinceId')
            citys, areas = get_citys_areas_by_provinceid(provinceId)
            return JsonResponse({'citys': citys, 'areas': areas})


        elif type == '2':

            cityId = request.POST.get('cityId')

            areas = get_areas_by_cityid(cityId)

            return JsonResponse({'areas': areas})
        elif type == '3':

            name = request.POST['name']

            phone = request.POST['phone']

            address = request.POST['address']

            user = request.session.get('user')

            Address.objects.create(uname=name, phone=phone, address=address, user=user,
                                   isdefault=(lambda count: True if count == 0 else False)(user.address_set.count()))

            addresses = []

            for address1 in Address.objects.all():
                name = address1.uname

                phone = address1.phone

                address, details = (lambda a: (''.join(a[:-1]), ''.join(a[-1])))(address1.address.split(','))

                addresses.append(html.format(name=name, phone=phone, address=address, details=details))

            return JsonResponse({'addresses': addresses})





