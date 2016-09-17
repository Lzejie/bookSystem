# coding:utf8
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name',max_length=30)

class Login(forms.Form):
    username = forms.CharField(label="用户名",max_length=30)
    password = forms.CharField(label="密码",widget=forms.PasswordInput())

class Regist(forms.Form):
    username = forms.CharField(label="用户名",max_length=30)
    password = forms.CharField(label="密码",max_length=30,widget=forms.PasswordInput())
    makesure = forms.CharField(label="确认密码",max_length=30,widget=forms.PasswordInput())

class Suggestion(forms.Form):
    content = forms.CharField(label="建议:",widget=forms.Textarea)

class ChangePassword(forms.Form):
    oldpassword = forms.CharField(label="请输入旧密码",max_length=30,widget=forms.PasswordInput())
    newpassword = forms.CharField(label="请输入新密码",max_length=30,widget=forms.PasswordInput())
    makesure = forms.CharField(label="确认密码",max_length=30,widget=forms.PasswordInput())

# 检索框
class Search(forms.Form):
    search = forms.CharField(max_length=30)
