from django.urls import path
from .views import create_list_post_comment, like_unlike, DeletePost, UpdatePost

app_name = 'post'

urlpatterns = [
    path('', create_list_post_comment, name='create_list_post_comment'),
    path('liked/', like_unlike, name='like_unlike'),
    path('<pk>/delete', DeletePost.as_view(), name='delete-post'),
    path('<pk>/update', UpdatePost.as_view(), name='update-post'),
]