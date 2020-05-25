
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
from .models import Article, Menu, Category, Author
from .forms import Blog_login, Blog_register
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # - 倒叙从大到小， 不加则是顺序从小到大

    articles = Article.objects.all().order_by('-create_time')
    menus = Menu.objects.all()
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

def register(request):
    if request.method == "POST":
        form = Blog_register(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            phone = form.cleaned_data.get('phone')
            print(f"username: {username}, password:{password}")
            # 使用内置自带的create_user 方法创建用户， 不需要save,
            user = User.objects.create_user(username=username, password=password, email=email)
            author = Author(author_name=user, phone=phone)
            author.save()
            return redirect(reverse('blog:login'))
    else:
        form = Blog_register()

    return render(request, 'blog/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = Blog_login(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if  user.is_active:
                auth.login(request, user)
                return redirect(reverse('blog:user', args=[user.id]))
        else:
            return render(request, 'blog/login.html', {'form': form, 'message':'Wrong account or password, Please try again.'})
    else:
        form = Blog_login()
    return render(request, 'blog/login.html', {'form':form})


@login_required
def user(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'blog/user.html', {'user': user})

    # if user.username == request.user:
    #     return render(request, 'blog/user.html', {'user':user})
    # else:
    #     form = Blog_login()
    #     return render(request, 'blog/login.html', {'form': form})