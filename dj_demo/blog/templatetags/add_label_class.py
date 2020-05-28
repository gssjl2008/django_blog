# -*- coding: utf-8 -*-
# @Time    : 2020/5/25 22:04
# @Author  : wuxing
# @Email   : xingwu@iflytek.com
# @File    : add_label_class.py
# @desc    : 自定义命令

from django import template

register = template.Library()

@register.filter(is_safe=True)
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})

@register.simple_tag
def call_method(obj, method, *args):
    method = getattr(obj, method)
    return method(*args)