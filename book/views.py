# coding:utf8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext
from . import forms
from models import *
from django.contrib.auth import authenticate, login, logout
# 方位某个视图需要用户登陆,如果没登陆的话就会跳转到settings.LOGIN_URL中,如果已经登陆就正常执行
from django.contrib.auth.decorators import login_required, user_passes_test
# 分页用的
from django.core.paginator import Paginator, EmptyPage,InvalidPage,PageNotAnInteger


# Create your views here.
def index(request):
    page = request.GET.get('page',1)
    books = Book.objects.all()
    p = Paginator(books,2)
    uf = forms.Search()
    try:
        booklist = p.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        booklist = p.page(1)
    return render(request, 'firstpage.html', {'books': booklist,'uf':uf,'STATIC_URL':' static/'})


def user_login(request):
    if request.method == "POST":
        nextpage = request.GET.get("next")
        print(nextpage)
        uf = forms.Login(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # if nextpage :
                    #     return render_to_response(nextpage)
                    return HttpResponse("登陆成功")
            else:
                return HttpResponse("账号不存在")
    else:
        uf = forms.Login()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))


def user_logout(request):
    logout(request)
    return HttpResponse("登出成功")

# user_passes_test 是用来检测已登陆的用户的某些信息的,function 是用来验证的信息
# 会将request.user传到function中
# 不通过的将会重定向到login界面
# def check(user):
#     if user.username == 'GGG':
#         return False
#     return True
# @user_passes_test(check,login_url='/login')
def regist(request):
    print "regist"
    if request.user.username:
        return HttpResponse("登陆状态无法注册")
    if request.method == "POST":
        uf = forms.Regist(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data["username"]
            password = uf.cleaned_data["password"]
            if authenticate(username=username,password=password) is not None:
                return HttpResponse("用户名已存在")
            else:
                user = User.objects.create_user(username=username,password=password)
                user.save()
                return HttpResponse('注册成功')
    else:
        uf = forms.Regist()
    return render_to_response('regist.html',{'uf':uf},context_instance=RequestContext(request))

# 提建议
@login_required(login_url='/login')
def user_suggestion(request):
    if request.method == 'POST':
        uf = forms.Suggestion(request.POST)
        if uf.is_valid():
            content = uf.cleaned_data['content']
            user = request.user
            sug = Suggestion.objects.create(user=user,suggestion=content)
            sug.save()
            return HttpResponse('提交成功')
    else:
        uf = forms.Suggestion()
    return render_to_response('suggestion.html',{'uf':uf},context_instance=RequestContext(request))

# 图书详细信息页
def bookinfo(request):
    bookid = request.GET.get("id",1)
    try:
        info = Book.objects.get(id=bookid)
    except Book.DoesNotExist:
        info = '未找到该书信息'
    return render(request, 'bookinfo.html', {'book':info,'STATIC_URL':' static/'})

# 用户资料页
@login_required(login_url='/login')
def user_info(request):
    userid = request.user.id
    user = User.objects.get(id=userid)
    username = user.username
    password = user.password
    lend = user.lend
    comment = user.comment
    score = user.score
    mylist = user.booklist
    suggestion = user.suggestion
    remind = user.remind
    collection = user.collection

    return render(request,'userinfo.html',{'password':password,'lend':lend,'comment':comment,'score':score,
                                           'mylist':mylist,'suggestion':suggestion,'remind':remind,
                                           'username':username,'collection':collection})


# 修改密码
@login_required(login_url='/login')
def mypassword(request):
    if request.method == "POST":
        uf = forms.ChangePassword(request.POST)
        if uf.is_valid():
            oldpassword = uf.cleaned_data['oldpassword']
            newpassword = uf.cleaned_data['newpassword']
            makesure = uf.cleaned_data['makesure']
            if makesure!= newpassword:
                return HttpResponse('两次输入不相同,请重新确认密码')
            user = authenticate(username=request.user.username, password=oldpassword)
            if user is not None:
                if user.is_active:
                    user.set_password(newpassword)
                    user.save()
                    return HttpResponse("密码修改成功~")
            else:
                return HttpResponse("旧密码输入错误")
    else:
        uf = forms.ChangePassword()
    return render_to_response('mypassword.html',{'uf':uf},context_instance=RequestContext(request))

# 我借的书
@login_required(login_url='/login')
def mylend(request):
    user = request.user
    lend = user.lend
    return render(request,'mylend.html',{'lend':lend})

# 搜索结果界面
def search(request):
    page = request.GET.get('page',1)
    key = request.GET.get('key','')
    print key
    list = Book.objects.filter(name__icontains=key)
    print list
    # return HttpResponse('------')
    p = Paginator(list, 15)
    try:
        booklist = p.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        booklist = p.page(1)
    return render(request, 'searchpage.html', {'key':key,'list': booklist,'STATIC_URL':' static/'})


# 我的评论
@login_required(login_url='/login')
def mycomment(request):
    user = request.user
    comment = user.comment
    return render(request,'mycomment.html', {'comment': comment})

# 我的评分
@login_required(login_url='/login')
def myscore(request):
    user = request.user
    score = user.score
    return render(request,'myscore.html',{'score':score})

# 我的书单
@login_required(login_url='/login')
def mybooklist(request):
    user = request.user
    booklist = user.booklist
    return render(request,'mybooklist.html',{'booklist':booklist})

# 我的建议
@login_required(login_url='/login')
def mysuggestion(request):
    user = request.user
    suggestion = user.suggestion
    return render(request,'mysuggestion.html',{'suggestion':suggestion})

# 我的提醒
@login_required(login_url='/login')
def myremind(request):
    user = request.user
    remind = user.remind
    return render(request,'myremind.html',{'remind':remind})

# 我的收藏
@login_required(login_url='/login')
def mycollection(request):
    user = request.user
    collection = user.collection
    return render(request,'mycollection.html',{'collection':collection})

# 获取热门书籍
def gethot():
    pass

# 获取新书
def getnew():
    pass

# 获取相似图书
def getsimiller():
    pass

# 获取个性化图书
def getpersional():
    pass

# 获取书单
def getbooklist():
    pass




