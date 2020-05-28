# encoding: utf-8
#@author: wuxing
#@file: forms.py
#@time: 2020/5/25 10:25
#@desc:

from django.contrib import auth
from django.contrib.auth.models import User
from django import forms
import re

#      验证流程：
#         1.调用了该is_valid方法 
#         2.执行了self.full_clean()
#         3.执行了self_clean_fields（开始字段匹配验证）
#         4.执行源码的 self._clean_form()#执行该的方法（我们可以自定义）（支持异常，直接返回异常）
#         5.执行源码的 self._post_clean()#执行该的方法（我们可以自定义）（不允许直接返回异常，需要调用add_error方法把异常作为实参进行有效返回）
#         6.is_valid进行赋值：只有2个一个是true代表数据正确，一个是false：代表数据错误
#         7.url对应函数里面进行判断id_valid
#         8.正确通过obj.clean进行获取 错误的话通过obj.errors获取

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class Blog_register(forms.Form):
    # 所有的数据流会经过clean()这个函数
    '''
    required=True,               是否允许为空
    widget=None,                 HTML插件, 可以设置class
    label=None,                  用于生成Label标签或显示内容
    initial=None,                初始值
    help_text='',                帮助信息(在标签旁边显示)
    error_messages=None,         错误信息 {'required': '不能为空', 'invalid': '格式错误'}
    show_hidden_initial=False,   是否在当前插件后面再加一个隐藏的且具有默认值的插件（可用于检验两次输入是否一直）
    validators=[],               自定义验证规则
    localize=False,              是否支持本地化（根据不同语言地区访问用户显示不同语言）
    disabled=False,              是否可以编辑
    label_suffix=None            Label内容后缀
    '''
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.CharField(label='Phone', max_length=20, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class':'form-control'}))


    # self._clean_字段名()        # 针对单个字段预留的方法（也就是该字段通过form验证以后就会触发该对应名字的自定义方法）
    # self._clean_form()         # 针对多个字段预留的方法
    # self._post_clean()         # 针对多个字段预留的方法
    # self._clean_filed 会调用 自定义的 clean_字段 的函数来进行对应的字段校验。
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 6 characters long")
        elif len(username) > 50:
            raise forms.ValidationError("Username is too long")
        else:
            '''
            __exact 精确等于 like ‘aaa’
            __iexact 精确等于 忽略大小写 ilike ‘aaa’
            __contains 包含 like ‘%aaa%’
            __icontains 包含 忽略大小写 ilike ‘%aaa%’，但是对于sqlite来说，contains的作用效果等同于icontains。
            __gt 大于
            __gte 大于等于
            __lt 小于
            __lte 小于等于
            __in 存在于一个list范围内
            __startswith 以…开头
            __istartswith 以…开头 忽略大小写
            __endswith 以…结尾
            __iendswith 以…结尾，忽略大小写
            __range 在…范围内
            __year 日期字段的年份
            __month 日期字段的月份
            __day 日期字段的日
            __isnull=True/False
            __isnull=True 与 __exact=None的区别
            '''
            exist_user = User.objects.filter(username=username)
            #  username=username  自动转换为 username__exact=username 来进行执行！
            if len(exist_user):
                raise forms.ValidationError("Username is already exists!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            exist_eamil = User.objects.filter(email__exact=email)
            if exist_eamil:
                raise forms.ValidationError("Eamil is already exists!")
        else:
            raise forms.ValidationError("Please enter a valid email!")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("Password is too short!")
        elif len(password1) > 20:
            raise forms.ValidationError("Password is too long!")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if all([password1, password2]) and password1 != password2:
            raise forms.ValidationError("Password miss match, Please enter again!")
        return password2

class Blog_login(forms.Form):

    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}), )
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    # remember = forms.BooleanField(label='Remember me')

class Blog_update(forms.Form):

    origin_password = forms.CharField(label='Origin Password', max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='New Password', max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmation Password', max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # def clean_origin_password(self):
    #     origin_password = self.cleaned_data.get('origin_password')
    #     print(f"origin_password: {origin_password}")
    #     user = auth.authenticate(username=self.cleaned_data.get('username'), password=origin_password)
    #     print(f"user: {user}")
    #     if not user:
    #         raise forms.ValidationError("Password is wrong!")
    #     return origin_password

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("Password is too short!")
        elif len(password1) > 20:
            raise forms.ValidationError("Password is too long!")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if all([password1, password2]) and password1 != password2:
            raise forms.ValidationError("Password miss match, Please enter again!")
        return password2

class Article_form(forms.Form):

    title = forms.CharField(label='标题', max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    sub_title = forms.CharField(label='副标题', max_length=140, widget=forms.TextInput(attrs={'class':'form-control'}))
    overview = forms.CharField(label='概要', max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    text = forms.CharField(label='正文', widget=forms.TextInput(attrs={'class':'form-control'}))
    # category = forms.ChoiceField(choices=([1, ]))
    # tag = models.ManyToManyField(Tag, verbose_name='标签' ,related_name='tags', blank=True)