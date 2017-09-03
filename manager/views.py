from django.shortcuts import render, redirect
from web.models import Subscription


def index(request):
    try:
        subscript = Subscription.objects.get(id=request.GET['id'])
        data = []
        for val in subscript:
            data.append(val)
        return render(request, 'web/manager/index.html', {'data': data})
    except:
        return redirect('/web/')
