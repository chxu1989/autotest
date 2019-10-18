from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from apitest.models import Apitest, Apistep, Apis
import pymysql


# Create your views here.


# 登录动作
def login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/home/')
            return response
        else:
            return render(request, 'login.html', {'error': '用户名或者密码错误'})
    return render(request, 'login.html')


# @login_required
def home(request):
    # username=request.session.get('user','')
    return render(request, 'home.html')


def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


# 接口管理
@login_required
def apitest_manage(request):
    apitest_list = Apitest.objects.all()  # 读取所有流程接口
    username = request.session.get('user', '')  # 读取浏览器登录Session
    
    # 定义流程接口数据的变量并返回前端
    return render(request, 'apitest_manage.html', {'user': username, 'apitests': apitest_list})


# 接口步骤管理
@login_required
def apistep_manage(request):
    apistep_list = Apistep.objects.all()  # 读取所有流程接口
    username = request.session.get('user', '')  # 读取浏览器登录Session
    
    # 定义流程接口数据的变量并返回前端
    return render(request, 'apistep_manage.html', {'user': username, 'apisteps': apistep_list})


# 单一接口管理
@login_required
def apis_manage(request):
    apis_list = Apis.objects.all()  # 读取所有流程接口
    username = request.session.get('user', '')  # 读取浏览器登录Session
    
    # 定义流程接口数据的变量并返回前端
    return render(request, 'apis_manage.html', {'user': username, 'apis': apis_list})


# 测试报告管理
@login_required
def test_report(request):
    apis_list = Apis.objects.all()  # 读取所有流程接口
    apis_count = Apis.objects.all().count()
    username = request.session.get('user', '')  # 读取浏览器登录Session
    
    # 连接数据库，创建游标
    db = pymysql.connect(user='root', db='autotest', passwd='test123456', host='127.0.0.1')
    cursor = db.cursor()
    
    # 获取用例执行成功记录数
    sql1 = 'select count(id) from apitest_apis where apitest_apis.apistatus=1'
    aa = cursor.execute(sql1)
    apis_pass_count = [row[0] for row in cursor.fetchall(aa)[0]]
    
    # 获取用例执行失败记录数
    sql2 = 'select count(id) from apitest_apis where apitest_apis.apistatus=0'
    bb = cursor.execute(sql2)
    apis_fail_count = [row[0] for row in cursor.fetchall(bb)[0]]
    
    # 定义流程接口数据的变量并返回前端
    return render(request, 'report.html', {'user': username, 'apis': apis_list, 'apiscounts': apis_count,
                                           'apis_pass_counts': apis_pass_count, 'apis_fail_counts': apis_fail_count})
