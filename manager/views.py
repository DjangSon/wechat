from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from web.models import Subscription


def index(request):
    try:
        subscript = Subscription.objects.filter(id=request.GET['id']).values()
        data = []
        for val in subscript:
            data.append(val)
        return render(request, 'web/manager/index.html', {'data': data})
    except:
        return redirect('/web/logout/')


def message(request, wehcat_id):
    signature = request.GET['signature']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']
    if 'echostr' in request.GET:
        return HttpResponse(request.GET['echostr'])
    openid = request.GET['openid']

