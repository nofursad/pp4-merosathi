from django.shortcuts import render, redirect
from .models import Post, Like
from userprofile.models import Profile
from .forms import PostForm, CommentForm


# View to Create Post, comment post and like post
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

    return redirect('post:create_list_post_comment')