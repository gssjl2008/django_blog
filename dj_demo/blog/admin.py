from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db import models

# Register your models here.
# from .models import Author, Article, Tag, Category, Menu
# #
# for cls in [Article, Author, Tag, Category, Menu]:
#     print(f"cls: {cls}")
#     admin.site.register(cls)
# 动态增加models中的类
import importlib

# 修改后台标题
admin.site.site_header = 'Blog后台管理系统'

class Article_admin(admin.ModelAdmin):
    # admin页面上显示具体信息的字段
    list_display = ['title', 'author', 'category', 'modity_time', 'create_time']
    # 过滤项
    list_filter = ['author', 'category']
    # 每页显示的数量
    list_per_page = 5
    # 可编辑字段
    list_editable = ['category']
    # 按照日期筛选
    date_hierarchy = 'create_time'
    # 按照创建时间排序
    ordering = ('create_time', )
    # 新增信息时候显示可填写的字段
    # fields = ['title', 'sub_title', 'text']
    filter_horizontal = ['tag',]

    # 重写 save_model 方法， 作者信息为登陆的用户， 而不是随便填写的
    # request.user 则是登陆的用户
    # obj 则指的是 Article
    # def save_model(self, request, obj, form, change):
        # obj.author = request.user
        # super().save_model(request, obj, form, change)

class Menu_Admin(admin.ModelAdmin):
    list_display = ['name', 'rank']

clses = importlib.import_module('blog.models')

for cls in dir(clses):
    if cls in ('datetime', 'User'):
        continue
    if cls == 'Article':
        admin.site.register(getattr(clses, cls, None), Article_admin)
    elif cls == 'Menu':
        admin.site.register(getattr(clses, cls, None), Menu_Admin)
    else:
        cls = getattr(clses, cls, None)
        if isinstance(cls, type):
            try:
                admin.site.register(cls)
            except AlreadyRegistered:
                pass