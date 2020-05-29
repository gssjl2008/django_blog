from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.timezone import datetime



class Author(models.Model):
    '''
    一对一 User，默认User字段
        username：用户名
        email: 电子邮件
        password：密码
        first_name：名
        last_name：姓
        is_active: 是否为活跃用户。默认是True
        is_staff: 是否为员工。默认是False
        is_superuser: 是否为管理员。默认是False
        date_joined: 加入日期。系统自动生成

    扩展添加
        phone: 手机号码
        mod_time: 修改时间
    '''
    author_name = models.OneToOneField(User, max_length=50, on_delete=models.CASCADE, related_name='author')
    phone = models.CharField(verbose_name='手机号码', max_length=20)
    # auto_now 系统自动生成， 也就是不能再手动给它存非当前时间的值
    # auto_now_add 每次修改则会更新时间, 可以设置其他值
    # update 和 save 都无法更改 auto_now_add 的值， 而 save 可改变 auto_now 的值
    # auto_now 一般用于 修改时间， auto_now_add 一般用于创建时间
    # 以上两个选项都不会出现再注册页面， 如需要显示，则需要设置属性 mod_time.editable = True 即可。
    mod_time = models.DateTimeField(verbose_name='修改时间', blank=True, auto_now=True)


    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = verbose_name
        # ordering = (User.date_joined,)

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
    views = models.PositiveIntegerField(verbose_name='阅读量', default=0)

    def get_absolute_url(self):
        '''
        通过此处构造url， 模板变动更少。
        :return:
        '''
        from django.urls import reverse
        return reverse('blog:article', args=[str(self.id)])

    # 自动记录阅读数量
    def add_view(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.title

class Menu(models.Model):

    name = models.CharField(verbose_name='菜单名称', max_length=20)
    rank = models.IntegerField(verbose_name='菜单排名', auto_created=True, unique=True)
    method = models.CharField(verbose_name='菜单方法', max_length=20, blank=True)

    def get_method_url(self, name=None):
        from django.urls import reverse
        if self.method in ('user', 'update'):
            return reverse('blog:%s' %self.method, args=[name])
        return reverse('blog:%s' %self.method)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = verbose_name
        ordering = ['rank']

    def __str__(self):
        return self.name
