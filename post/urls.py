from django.urls import path
from .views import create_list_post_comment, like_unlike

app_name = 'post'

urlpatterns = [
    path('', create_list_post_comment, name='create_list_post_comment'),
    path('liked/', like_unlike, name='like_unlike'),
]