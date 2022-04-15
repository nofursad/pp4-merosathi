from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .utilities import get_random_username_addon
from django.template.defaultfilters import slugify
from cloudinary.models import CloudinaryField
from django.db.models import Q

class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Friendship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = []
        for fs in qs:
            if fs.status == 'accepted':
                accepted.append(fs.receiver)
                accepted.append(fs.sender)
        
        available = [profile for profile in profiles if profile not in accepted]
        return available

    def get_all_profile(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles



class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="No Bio...", max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = CloudinaryField('image', default='blank-avatar_pxjsla.png')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def get_absolute_url(self):
        return reverse('userprofile:user_profile_view', kwargs={'slug': self.slug})

    def friends_list(self):
        return self.friends.all()

    def total_friends(self):
        return self.friends.all().count()

    def total_posts(self):
        return self.posts.all().count()

    def get_all_post(self):
        return self.posts.all()

    def total_likes_given(self):
        likes = self.like_set.all()
        total_likes = 0
        for item in likes:
            if item.value == 'Like':
                total_likes += 1
        return total_likes

    def total_likes_received(self):
        posts = self.posts.all()
        total_likes = 0
        for item in posts:
            total_likes += item.liked.all().count()
        return total_likes


    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        temp_slug = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug == '':
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                temp_slug = Profile.objects.filter(slug=to_slug).exists()
                while temp_slug:
                    to_slug = slugify(to_slug + " " + str(get_random_username_addon()))
                    temp_slug = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

class FriendshipManager(models.Manager):
    def request_received(self, receiver):
        request_list = Friendship.objects.filter(receiver=receiver, status='send')
        return request_list

    def request_send(self, sender):
        all_profiles = Friendship.objects.filter(sender=sender, status='send')
        return all_profiles

class Friendship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models. CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = FriendshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
