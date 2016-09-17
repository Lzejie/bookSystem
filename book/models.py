# coding:utf8

from __future__ import unicode_literals
from django.db import models
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import User


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(default='111111', max_length=30)
    # 用户当前状态
    status = models.IntegerField(default=0)
    age = models.IntegerField(null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=1000)
    id = models.CharField(max_length=15, primary_key=True)
    # price = models.FloatField(default=50)
    author = models.CharField(max_lengtd=1000)
    # count = models.IntegerField(default=3)
    # pos = models.CharField(max_length=300, null=True, default='No inforation')
    publicYear = models.IntegerField(default=2000)
    publisher = models.CharField(max_length=1000,default='XXXXXX')
    pic_s = models.CharField(max_length=500,default='...')
    pic_m = models.CharField(max_length=500,default='...')
    pic_b = models.CharField(max_length=500,default='...')
    # createdAt = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        name = '书名:' + str(self.title)
        return name


class Lend(models.Model):
    # 用户外键
    user = models.ForeignKey(User,related_name="lend")
    # 图书外键
    book = models.ForeignKey(Book,related_name="lend")
    # 是否续借
    renew = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    returnAt = models.DateField(null=True)

    def __unicode__(self):
        return '借出时间:'+str(self.createdAt)


class Score(models.Model):
    score = models.IntegerField()
    # 用户外键
    user = models.ForeignKey(User,related_name="score")
    # 图书外键
    book = models.ForeignKey(Book,related_name="score")
    createdAt = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    # 图书外键
    book = models.ForeignKey(Book,related_name="comment")
    # 用户外键
    user = models.ForeignKey(User,related_name="comment")
    comment = models.CharField(max_length=500)
    createdAt = models.DateTimeField(auto_now_add=True)

class Suggestion(models.Model):
    # 用户外键
    user = models.ForeignKey(User,related_name="suggestion")
    suggestion = models.CharField(max_length=500)
    createdAt = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.user)+' 建议 '+str(self.suggestion)

# 收藏的图书
class Collection(models.Model):
    # 用户外键
    user = models.ForeignKey(User,related_name="collection")
    # 图书外键
    book = models.ForeignKey(Book,related_name='collection')
    createdAt = models.DateTimeField(auto_now_add=True)


# 书单
class BookList(models.Model):
    # 用户外键
    user = models.ForeignKey(User,related_name="booklist")
    name = models.CharField(max_length=30)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


# 书单列表
class BookListItem(models.Model):
    # 图书外键
    book = models.ForeignKey(Book, related_name="booklistitem")
    # 书单外键
    booklist = models.ForeignKey(BookList, related_name="item")
    createdAt = models.DateTimeField(auto_now_add=True)

class Search(models.Model):
    # 用户外键
    user = models.ForeignKey(User,related_name="search")
    message = models.CharField(max_length=30)
    createdAt = models.DateTimeField(auto_now_add=True)

# 公告
class Notice(models.Model):
    # 用户外键
    user = models.ForeignKey(User,related_name="notice")
    message = models.CharField(max_length=5000)
    createdAt = models.DateTimeField(auto_now_add=True)

# 标签
class Label(models.Model):
    name = models.CharField(max_length=15)
    createdAt = models.DateTimeField(auto_now_add=True)

class BookManagement(models.Model):
    # 图书外键
    book = models.ForeignKey(Book,related_name="management")
    # 用户外键
    user = models.ForeignKey(User,related_name="management")
    # 图书数量变化情况
    count = models.IntegerField()
    info = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True)


class Click(models.Model):
    # 图书外键
    book = models.ForeignKey(Book,related_name="click")
    # 用户外键
    user = models.ForeignKey(User,related_name="click")
    createdAt = models.DateTimeField(auto_now_add=True)


# 设置来书提醒
class Remind(models.Model):
    # 图书外键
    book = models.ForeignKey(Book,related_name="remind")
    # 用户外键
    user = models.ForeignKey(User,related_name="remind")
    # 是否已经提醒了
    status = models.BooleanField()
    createdAt = models.DateTimeField(auto_now_add=True)

