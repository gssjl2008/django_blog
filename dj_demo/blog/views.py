from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Article, Menu, Category

def index(request):
    # - 倒叙从大到小， 不加则是顺序从小到大
    articles = Article.objects.all().order_by('-create_time')
    menus = Menu.objects.all().order_by('-rank')
    categories = Category.objects.all()
    return render(request, 'blog/index.html', {'articles': articles, 'menus': menus, 'categories':categories})


def article(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'blog/article.html', {'article': article})


def admin(request):
    return render(request, 'blog/admin.html')


def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')