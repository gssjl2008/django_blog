from django.http.response import JsonResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.generic import ListView, DetailView, FormView

# Create your views here.
from .models import Article, Menu, Category, Author
from .forms import Blog_login, Blog_register, Blog_update
from django.contrib.auth.decorators import login_required

# @login_required
# def index(request):
#     # - 倒叙从大到小， 不加则是顺序从小到大
#
#     articles = Article.objects.all().order_by('-create_time')
#     menus = Menu.objects.all()
#     categories = Category.objects.all()
#     return render(request, 'blog/index.html', {'articles': articles, 'menus': menus, 'categories':categories})

class Index_view(ListView):

    template_name = 'blog/index.html'
    context_object_name = 'articles'
    # 等同于 articles = Article.objects.all(), 赋予的变量默认为 object_list或article_list, 返回的模板名称 app_name/model_name_list.html, 可以使用
    model = Article

    def get_context_data(self, *, object_list=None, **kwargs):
        '''
        增加返回的属性,比如menu菜单类
        '''
        menus = Menu.objects.all()
        categories = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['menus'] = menus
        context['categories'] = categories
        return context

    def get_queryset(self):
        '''
        过滤用户只能看到自己的文章,
        '''
        # if self.request.user.username == 'root':
        #     super().get_queryset()
        # else:
        return Article.objects.filter(id=self.request.user.id)



@login_required
def article(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'blog/article.html', {'article': article})

@login_required
def admin(request):
    return render(request, 'blog/admin.html')

@login_required
def about(request):
    return render(request, 'blog/about.html')

@login_required
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
            if  user is not None and user.is_active:
                auth.login(request, user)
                return redirect(reverse('blog:user', args=[user.username]))
            else:
                return render(request, 'blog/login.html', {'form': form, 'message':'Wrong account or password, Please try again.'})
    else:
        form = Blog_login()
    return render(request, 'blog/login.html', {'form':form})


@login_required
def user(request, name):
    if request.user.username == name:
        user = get_object_or_404(User, username=name)
        return render(request, 'blog/user.html', {'user': user})
    else:
        raise Http404()

@login_required
def update(request, name):
    print(f"request.user: {request.user}, {dir(request)}")
    user = get_object_or_404(User, username=name)
    form = Blog_update(request.POST)
    if form.is_valid():
        password1 = form.cleaned_data.get('password1')
        user.set_password(password1)
        user.save()
        #return render(request, 'blog/update.html', {'form': form, 'text':'Change Password!'})
    else:
        form = Blog_update()
    return render(request, 'blog/update.html', {'form': form, 'text': 'Change Password!'})

def logout(request, name):
    auth.logout(request)
    return redirect(reverse('blog:login'))
