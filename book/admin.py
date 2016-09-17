# coding:utf8
from django.contrib import admin
from . import models

# Register your models here.

# 如果定义了该类,并且在引入时在后面加上该类
# 则fields后面表示展示的数据以及顺序
class UserInfo(admin.ModelAdmin):
    fields = ['state','name']

admin.site.register(models.Book)
# admin.site.register(models.Suggestion)
# admin.site.register(models.Type)




