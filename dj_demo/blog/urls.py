# encoding: utf-8
#@author: wuxing
#@file: urls.py
#@time: 2020/5/21 14:13
#@desc:

from django.urls.conf import path
from .views import index, article

app_name = 'blog'
urlpatterns = [
    path('', index, name='index'),
    path('article/<int:id>', article, name='article')
]