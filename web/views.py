from django.shortcuts import render
from django.http.response import JsonResponse

# Create your views here.


def index(request):
    if request.session. has_key('web'):
        return render(request, 'web/index.html')
    else:
        return render(request, 'web/login.html')


def login(request):
    request.session['web'] = '1'
    return JsonResponse({'error': 1, 'msg': '登陆成功'})
    # return redirect('web/index.html')
