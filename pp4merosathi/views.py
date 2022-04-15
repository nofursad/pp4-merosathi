# from django.http import HttpResponse
from django.shortcuts import render
from allauth.account.forms import LoginForm


def home_page(request):
    # return HttpResponse('Hello World!')
    form = LoginForm(request.POST or None)

    context = {
        'form': form,
    }
    return render(request, 'account/login.html', context)