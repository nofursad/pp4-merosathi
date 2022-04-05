from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import FileExtensionValidator
from userprofile.models import Profile

class Post(models.Model):
    content = models.TextField()
    image = CloudinaryField('image', validators=[FileExtensionValidator(['png', 'jpeg', 'jpg', 'gif'])], blank=True)
    liked = models.ManyToManyField(Profile, default=None, related_name='likes')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post')


    def __str__(self):
        return str(self.content[:20])

    def total_likes(self):
        return self.liked.all().count()


    # Total number of comment

    class Meta:
        ordering = ('-created_on',)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"