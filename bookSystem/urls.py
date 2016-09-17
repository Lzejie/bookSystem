"""bookSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from book import views as bookView
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login',bookView.user_login,name="login"),
    url(r'^regist',bookView.regist,name='regist'),
    url(r'^mypassword',bookView.mypassword,name='mypassword'),
    url(r'^logout',bookView.user_logout,name='logout'),
    url(r'^suggestion',bookView.user_suggestion,name='suggestion'),
    url(r'^bookinfo',bookView.bookinfo,name='bookinfo'),
    url(r'^search',bookView.search,name='search'),
    url(r'^userinfo',bookView.user_info,name='userinfo'),
    # url(r'^bookinfo',bookView.bookinfo,name='bookinfo'),
    url(r'^mybooklist',bookView.mybooklist,name='mybooklist'),
    url(r'^mycollection',bookView.mycollection,name='mycollection'),
    url(r'^mycomment',bookView.mycomment,name='mycomment'),
    url(r'^mylend',bookView.mylend,name='mylend'),
    url(r'^myremind',bookView.myremind,name='myremind'),
    url(r'^myscore',bookView.myscore,name='myscore'),
    url(r'^mysuggestion',bookView.mysuggestion,name='mysuggestion'),
    url(r'^', bookView.index),
]
