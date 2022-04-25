from django.shortcuts import render, redirect
from allauth.account.forms import LoginForm


def home_page(request):
    if request.user.is_authenticated:
        user = request.user
        context = {
            'user': user
        }
        # return render(request, 'userprofile/profilepage.html', context)
        return redirect('/post', context)
    else:
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'account/login.html', context)
