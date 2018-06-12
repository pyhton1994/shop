#coding=utf-8
from django.core.paginator import Paginator
#分页工具函数
def get_objects_page(object_list=None,pagenum=1,perpage=12):
    print pagenum

    pages = Paginator(object_list=object_list,per_page=perpage)
    pagenum = int(pagenum)

    if pagenum<1:pagenum = 1

    if pagenum >pages.num_pages:pagenum = pages.num_pages

    page = pages.page(pagenum)

    return page,page.object_list












