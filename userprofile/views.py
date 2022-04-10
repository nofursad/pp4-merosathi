from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Friendship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q



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
    result = list(map(lambda x: x.sender, request_list))
    is_empty = False
    if len(result) == 0:
        is_empty = True

    context = {'request_list': result, 'is_empty': is_empty, }

    return render(request, 'userprofile/request.html', context)

def accept_request(request):
    if request.method=='POST':
        pk = request.POST.get('request_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        req = get_object_or_404(Friendship, sender=sender, receiver=receiver)
        if req.status == 'send':
            req.status = 'accepted'
            req.save()
    
    return redirect('userprofile:request_received_view')


def reject_request(request):
    if request.method=='POST':
        pk = request.POST.get('request_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        req = get_object_or_404(Friendship, sender=sender, receiver=receiver)
        req.delete()

    return redirect('userprofile:request_received_view')


def request_profiles_list_view(request):
    user = request.user
    all_profiles = Profile.objects.get_all_profiles_to_invite(user)

    context = {'all_profiles': all_profiles}

    return render(request, 'userprofile/torequest.html', context)

def profiles_list_view(request):
    user = request.user
    all_profiles = Profile.objects.get_all_profile(user)

    context = {'all_profiles': all_profiles}

    return render(request, 'userprofile/allprofiles.html', context)

class UserProfileView (DetailView):
    model = Profile
    template_name = 'userprofile/userdetail.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        req_r = Friendship.objects.filter(sender=profile)
        req_s = Friendship.objects.filter(receiver=profile)
        req_receiver = []
        req_sender = []
        for item in req_r:
            req_receiver.append(item.receiver.user)
        for item in req_s:
            req_sender.append(item.sender.user)
        context['req_receiver'] = req_receiver
        context['req_sender'] = req_sender
        context['posts'] = self.get_object().get_all_post()
        context['len_posts'] = True if len(self.get_object().get_all_post()) > 0 else False

        return context


class ProfileListView(ListView):
    model = Profile
    template_name = 'userprofile/allprofiles.html'
    context_object_name = 'all_profiles'

    def get_queryset(self):
        all_profiles = Profile.objects.get_all_profile(self.request.user)
        return all_profiles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        req_r = Friendship.objects.filter(sender=profile)
        req_s = Friendship.objects.filter(receiver=profile)
        req_receiver = []
        req_sender = []
        for item in req_r:
            req_receiver.append(item.receiver.user)
        for item in req_s:
            req_sender.append(item.sender.user)
        context['req_receiver'] = req_receiver
        context['req_sender'] = req_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

def send_request(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        fs = Friendship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('userprofile:profile_page_view')

def unfriend(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        fs = Friendship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
            )
        fs.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('userprofile:profile_page_view')
