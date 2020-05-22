from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

# Register your models here.

# from .models import Author, Article, Tag, Category, Menu
# #
# for cls in [Article, Author, Tag, Category, Menu]:
#     print(f"cls: {cls}")
#     admin.site.register(cls)
# 动态增加models中的类
import importlib

clses = importlib.import_module('blog.models')

for cls in dir(clses):
    cls = getattr(clses, cls, None)
    if isinstance(cls, type):
        try:
            admin.site.register(cls)
        except AlreadyRegistered:
            pass