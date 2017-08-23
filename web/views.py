from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth.hashers import check_password
from web.models import Users
from web.models import Subscription
from django.core.paginator import Paginator
from math import ceil
from time import time
from tool.models import upload
# Create your views here.


def index(request):
    if request.session. has_key('username') and request.session['status'] == 1:
        return render(request, 'web/index.html')
    else:
        return render(request, 'web/login.html')


def subscription(request):
    if request.session. has_key('username') is False:
        return redirect('/web')
    return render(request, 'web/subscription.html')


def wechat_list(request):
    wechats = Subscription.objects.all()
    count = wechats.count()
    paginator = Paginator(wechats, 15)
    data = {}
    try:
        temp = paginator.page(ceil(request.POST['start']/15) + 1)
    except:
        temp = paginator.page(1)
    for val in temp:
        data[val['id']] = val
    return JsonResponse({'draw': request.POST['draw'], 'recordsTotal': count, 'recordsFiltered': count, 'data': data})


def add_wechat(request):
    try:
        head_img = time()
        return JsonResponse({'data': request.POST['head_img']})
        # if upload('we-picture', '')
        wechat = Subscription(
            name=request.POST['name'], describe=request.POST['describe'], account=request.POST['account'],
            origin_id=request.POST['origin_id'], app_id=request.POST['app_id'], app_secret=request.POST['app_secret'],
            token=request.POST['token'], encodingaeskey=request.POST['encodingaeskey'], type=request.POST['type'],
        )
        return JsonResponse({'error': 0, 'msg': '添加成功'})
    except:
        return JsonResponse({'error': 1, 'msg': '参数异常'})


def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = Users.objects.get(username=username)
        if check_password(password, user.password):
            request.session['id'] = user.id
            request.session['username'] = user.username
            request.session['group_id'] = user.group_id
            request.session['status'] = user.status
            return JsonResponse({'error': 0, 'msg': '登陆成功'})
        else:
            return JsonResponse({'error': 1, 'msg': '密码错误'})
    except:
        return JsonResponse({'error': 1, 'msg': '用户不存在'})


def logout(request):
    try:
        del request.session['username']
    finally:
        return redirect('/web')
