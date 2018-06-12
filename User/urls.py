#coding=utf-8
from django.conf.urls import url
import views
urlpatterns = [
    url(r'^register',views.Register.as_view()),
    url(r'^usercenter/$',views.UserCenterView.as_view()),
    url(r'^login/$',views.Login.as_view()),
    url(r'^vcode/$', views.Code.as_view()),
    url(r'^checkcode/$', views.CheckCode.as_view()),
    url(r'^logout/$', views.Logout.as_view()),
    url(r'^address/$',views.UserAddressView.as_view()),
]