#coding=utf-8
from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$', views.CartView.as_view()),
    url(r'^cart.html$', views.CartListView.as_view()),
]