from django.urls import path
from .views import profile_page_view, request_received_view, profiles_list_view, request_profiles_list_view


app_name = 'userprofile'

urlpatterns = [
    path('profilepage/', profile_page_view, name='profile_page_view'),
    path('request/', request_received_view, name='request_received_view'),
    path('allprofiles/', profiles_list_view, name='profiles_list_view'),
    path('torequest/', request_profiles_list_view, name='request_profiles_list_view'),
]