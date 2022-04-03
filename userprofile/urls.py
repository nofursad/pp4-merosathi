from django.urls import path
from .views import profile_page_view


app_name = 'userprofile'

urlpatterns = [
    path('profilepage/', profile_page_view, name='profile_page_view')
]