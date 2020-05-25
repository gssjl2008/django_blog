# encoding: utf-8
#@author: wuxing
#@file: urls.py
#@time: 2020/5/21 14:13
#@desc:

from django.urls.conf import path
from .views import index, article, admin, about, contact, login, register, user

app_name = 'blog'
urlpatterns = [
    path('', index, name='index'),
    path('article/<int:id>', article, name='article'),
    path('admin', admin, name='admin'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('user/<id>', user, name='user'),
]