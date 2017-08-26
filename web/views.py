from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.contrib.auth.hashers import check_password
from web.models import Users
from web.models import Subscription
from django.core.paginator import Paginator
from math import ceil
from time import time
from base64 import b64decode
from wechatInterface.models import access_token, get_all_fans
from tool.models import upload, base64_decode
import datetime
# Create your views here.


def index(request):
    if request.session. has_key('username') and request.session['status'] == 1:
        return render(request, 'web/index.html')
    else:
        return render(request, 'web/login.html')


def subscription(request):
    if request.session. has_key('username') is False:
        return redirect('/web')
    return render(request, 'web/wechat/subscription.html')


def add_page(request):
    return render(request, 'web/wechat/page.html')


def wechat_list(request):
    wechats = Subscription.objects.all().values()
    count = wechats.count()
    paginator = Paginator(wechats, 15)
    data = []
    i = 0
    try:
        temp = paginator.page(ceil(request.POST['start']/15) + 1)
    except:
        temp = paginator.page(1)
    for val in temp:
        data.append(val)
        i += 1
    return JsonResponse({'draw': request.POST['draw'], 'recordsTotal': count, 'recordsFiltered': count, 'data': data})


def add_wechat(request):
    try:
        head_img = str(time()) + '_head_img.jpg'
        qrcode_img = str(time()) + '_qrcode_img.jpg'
        data = base64_decode(request.POST['head_img'])
        if data is False:
            return JsonResponse({'error': 1, 'msg': '图片格式错误'})
        upload('we-picture', head_img, b64decode(data))
        data = base64_decode(request.POST['qrcode_img'])
        if data is False:
            return JsonResponse({'error': 1, 'msg': '图片格式错误'})
        upload('we-picture', qrcode_img, base64_decode(data))
        now = datetime.datetime.now()
        wechat = Subscription(
            name=request.POST['name'], describe=request.POST['describe'], account=request.POST['account'],
            origin_id=request.POST['origin_id'], app_id=request.POST['app_id'], app_secret=request.POST['app_secret'],
            token=request.POST['token'], encodingaeskey=request.POST['encodingaeskey'], type=request.POST['type'],
            head_img=head_img, qrcode_img=qrcode_img, group_id=1, date_added=now.strftime('%Y-%m-%d %H:%M:%S')
        )
        wechat.save()
        return JsonResponse({'error': 0, 'msg': '添加成功'})
    except:
        return JsonResponse({'error': 1, 'msg': '参数异常'})


def get_access_token(request, wechat_id):
    try:
        wechat = Subscription.objects.get(id=wechat_id)
        result = access_token(app_id=wechat.app_id, app_secret=wechat.app_secret)
        wechat.access_token = result['access_token']
        wechat.last_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wechat.save()
        return JsonResponse({'error': 0, 'msg': '接入成功'})
    except:
        return JsonResponse({'error': 1, 'msg': '接入失败'})


def all_fans(request, wechat_id):
    try:
        access_token = Subscription.objects.get(id=wechat_id).access_token
        # get_all_fans()
    except:
        return '12'

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
