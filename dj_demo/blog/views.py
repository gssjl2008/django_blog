from django.http.response import JsonResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
from .models import Article, Menu, Category, Author
from .forms import Blog_login, Blog_register, Blog_update, Article_form


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
    queryset = Article.objects.all().order_by('-create_time')
    http_method_names = 'get'       # 限制使用的方法

    # model=Article 就这一句等同于 articles = Article.objects.all(), 赋予的变量默认为 object_list或article_list, 返回的模板名称 app_name/model_name_list.html, 使用类视图，上面可以的全局变量，可以定义这些默认值。
    model = Article

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
                return redirect(reverse('blog:user', args=[user.id]))
            else:
                return render(request, 'blog/login.html', {'form': form, 'message':'Wrong account or password, Please try again.'})
    else:
        form = Blog_login()
    return render(request, 'blog/login.html', {'form':form})

class Article_create_view(CreateView):
    model = Article
    template_name = 'blog/article_create.html'
    form_class = Article_form


class User_view(DetailView):

    template_name = 'blog/user.html'
    context_object_name = 'user'
    model = User

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(username__exact=self.request.user.username)

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

@login_required
def update(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = Blog_update(request.POST)

    if form.is_valid():
        user = auth.authenticate(username=user.username, password=form.cleaned_data.get('origin_password'))
        if user is not None:
            password1 = form.cleaned_data.get('password1')
            user.set_password(password1)
            user.save()
            return redirect(reverse('blog:login'))
        else:
            return render(request, 'blog/login.html',
                          {'form': form, 'message': 'Wrong account or password, Please try again.'})
    else:
        form = Blog_update()
        return render(request, 'blog/update.html', {'form': form, 'text': 'Change Password!', 'message':'Wrong password, Please try again.'})

