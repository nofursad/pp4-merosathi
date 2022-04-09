from django.shortcuts import render
from .models import Profile, Friendship
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

def request_received_view(request):
    user = Profile.objects.get(user=request.user)
    request_list = Friendship.objects.request_received(user)

    context = {'request_list': request_list}

    return render(request, 'userprofile/request.html', context)

def profiles_list_view(request):
    user = request.user
    all_profiles = Profile.objects.get_all_profile(user)

    context = {'all_profiles': all_profiles}

    return render(request, 'userprofile/allprofiles.html', context)

def request_profiles_list_view(request):
    user = request.user
    all_profiles = Profile.objects.get_all_profiles_to_invite(user)

    context = {'all_profiles': all_profiles}

    return render(request, 'userprofile/torequest.html', context)