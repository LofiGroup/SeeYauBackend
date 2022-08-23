from django.shortcuts import render


def index(request):
    return render(request, 'chat/index.html')


def room(request):
    token = request.GET.get('token', None)

    return render(request, 'chat/room.html', {'token': token})
