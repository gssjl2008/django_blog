from django.shortcuts import render

# Create your views here.
from .models import Article, Menu

def index(request):
    # - 倒叙从大到小， 不加则是顺序从小到大
    articles = Article.objects.all().order_by('-create_time')
    menus = Menu.objects.all().order_by('-rank')
    return render(request, 'blog/index.html', {'articles': articles, 'menus': menus})


def article(request, id):
    print(request, type(request), dir(request))
    return render(request, 'blog/article.html', {'article': Article.objects.get(id=id)})