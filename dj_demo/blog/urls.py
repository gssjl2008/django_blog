# encoding: utf-8
#@author: wuxing
#@file: urls.py
#@time: 2020/5/21 14:13
#@desc:

from django.urls.conf import path
from django.contrib.auth.views import LogoutView
from .views import Index_view, admin, about, contact, login, register, update, User_view, Article_view

app_name = 'blog'
urlpatterns = [
    # path('', index, name='index'),
    path('', Index_view.as_view(), name='index'),
    path('article/<int:pk>', Article_view.as_view(), name='article'),
    path('admin', admin, name='admin'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('user/<int:pk>', User_view.as_view(), name='user'),
    path('user/<int:pk>/update', update, name='update'),
    path('logout', LogoutView.as_view(), name='logout'),
]