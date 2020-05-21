from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Author(models.Model):

    author_name = models.OneToOneField(User, max_length=50, on_delete=models.CASCADE, related_name='author')
    phone = models.CharField(verbose_name='phone number', max_length=20)
    create_time = models.DateTimeField(verbose_name='create time', auto_created=True)


    class Meta:
        verbose_name = 'Author'
        ordering = ['create_time']

    def __str__(self):
        return self.author_name.username


class Tag(models.Model):

    name = models.CharField(verbose_name='article tag', max_length=20)

    class Meta:
        verbose_name = 'Tag'

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(verbose_name='article category', max_length=20)

    class Meta:
        verbose_name = 'category'

    def __str__(self):
        return self.name


class Article(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='article title', max_length=100)
    sub_title = models.CharField(verbose_name='article sub title', max_length=140, blank=True)
    overview = models.CharField(verbose_name='article overview', max_length=200, blank=True)
    text = models.TextField(verbose_name='article body')
    create_time = models.DateTimeField(verbose_name='article create time', auto_created=True)
    modity_time = models.DateTimeField(verbose_name='article modity time', auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    tag = models.ManyToManyField(Tag, related_name='tags', blank=True)

    class Meta:
        verbose_name = 'Article'
        ordering = ['create_time']

    def __str__(self):
        return self.title

class Menu(models.Model):
    name = models.CharField(verbose_name='menu name', max_length=20)
    rank = models.IntegerField(verbose_name='name rank', auto_created=True, unique=True)
    method = models.CharField(verbose_name='menu method', max_length=20, blank=True)

    class Meta:
        verbose_name = 'menu name'

    def __str__(self):
        return self.name
