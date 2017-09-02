from django.shortcuts import render


def index(request):
    return render(request, 'web/manager/index.html', {'id': request.GET['id']})
