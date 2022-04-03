from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    # return HttpResponse('Hello World!')
    user = request.user
    hello = 'Hello World!'

    context = {
        'user': user,
        'hello': hello
    }
    return render(request, 'main/index.html', context)