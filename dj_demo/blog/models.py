from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Author(models.Model):

    author_name = models.OneToOneField(User, max_length=50, on_delete=models.CASCADE, related_name='author')
    phone = models.CharField(verbose_name='手机号码', max_length=20)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_created=True)


    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = verbose_name
        ordering = ['create_time']

    def __str__(self):
        return self.author_name.username


class Tag(models.Model):

    name = models.CharField(verbose_name='标签', max_length=20)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(verbose_name='类别', max_length=20)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=100)
    sub_title = models.CharField(verbose_name='副标题', max_length=140, blank=True)
    overview = models.CharField(verbose_name='概要', max_length=200, blank=True)
    text = models.TextField(verbose_name='正文')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    modity_time = models.DateTimeField(verbose_name='修改时间', auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name='类型' ,on_delete=models.CASCADE, related_name='categories')
    tag = models.ManyToManyField(Tag, verbose_name='标签' ,related_name='tags', blank=True)

    def get_absolute_url(self):
        '''
        通过此处构造url， 模板变动更少。
        :return:
        '''
        from django.urls import reverse
        return reverse('blog:article', args=[str(self.id)])

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = verbose_name
        ordering = ['create_time']

    def __str__(self):
        return self.title

class Menu(models.Model):
    name = models.CharField(verbose_name='菜单名称', max_length=20)
    rank = models.IntegerField(verbose_name='菜单排名', auto_created=True, unique=True)
    method = models.CharField(verbose_name='菜单方法', max_length=20, blank=True)

    def get_method_url(self):
        from django.urls import reverse
        return reverse('blog:%s' %self.method)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
