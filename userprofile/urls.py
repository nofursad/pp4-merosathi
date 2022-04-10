from django.urls import path
from .views import (
    profile_page_view,
    request_received_view,
    profiles_list_view,
    request_profiles_list_view,
    ProfileListView,
    send_request,
    unfriend,
    accept_request,
    reject_request,
)


app_name = 'userprofile'

urlpatterns = [
    path('profilepage/', profile_page_view, name='profile_page_view'),
    path('request/', request_received_view, name='request_received_view'),
    path('allprofiles/', ProfileListView.as_view(), name='profiles_list_view'),
    path('torequest/', request_profiles_list_view, name='request_profiles_list_view'),
    path('send_request/', send_request, name='send_request'),
    path('unfriend/', unfriend, name='unfriend'),
    path('request/acceptrequest/', accept_request, name='accept_request'),
    path('request/rejectrequest/', reject_request, name='reject_request'),
]