#coding=utf-8


def user(request):
    return {'user':request.session.get('user')}