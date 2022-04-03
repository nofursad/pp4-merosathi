from django.shortcuts import render
from .models import Profile
from .forms import ProfileModelForm


def profile_page_view(request):
    user = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=user)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'user': user,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'userprofile/profilepage.html', context)
