from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Like
from userprofile.models import Profile
from .forms import PostForm, CommentForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# View to Create Post, comment post and like post
@login_required
def create_list_post_comment(request):
    post_content = Post.objects.all()
    profile = Profile.objects.get(user=request.user)


# form for posting and commenting
    post_form = PostForm()
    comment_form = CommentForm()
    posted = False

    profile = Profile.objects.get(user=request.user)

    if 'post_submit' in request.POST:
        print(request.POST)
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            post_form = PostForm()
            posted = True

    if 'comment_submit' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            comment_form = CommentForm()

    context = {
        'post_content': post_content,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'posted': posted,
    }

    return render(request, 'post/main.html', context)

@login_required
def like_unlike(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

            post_obj.save()
            like.save()

        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)

    return redirect('post:create_list_post_comment')


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/delete.html'
    success_url = reverse_lazy('post:create_list_post_comment')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.requeset, 'You are not author of the post')
        return obj


class UpdatePost(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post/update.html'
    success_url = reverse_lazy('post:create_list_post_comment')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You are not author of the post')
            return super().form_invalid(form)

# @login_required
# def user_post(request):
#     user = request.author.user
#     user_all_post = Post.objects.all().filter(author=user)

#     return user_all_post