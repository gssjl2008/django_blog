# encoding: utf-8
#@author: wuxing
#@file: urls.py
#@time: 2020/5/20 15:39
#@desc:


from django.urls import path
from .views import *

app_name = 'demo'
urlpatterns = [
    path('index', index, name='index'),
    path('admin', admin, name='admin')
]