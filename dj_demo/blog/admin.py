from django.contrib import admin

# Register your models here.

from .models import Author, Article, Tag, Category, Menu

for cls in [Article, Author, Tag, Category, Menu]:
    admin.site.register(cls)
