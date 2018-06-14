#coding=utf-8

from django.conf.urls import url
import views

urlpatterns=[
    url(r'^$', views.OrderView.as_view()),
    url(r'^order.html$', views.OrderListView.as_view()),
]

