from .models import Profile, Friendship

def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.avatar
        fname = profile_obj.first_name
        return {'picture': pic, 'fname': fname}
    return {}

def request_received_number(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        request_count = Friendship.objects.request_received(profile_obj).count()
        return {'request_num':request_count}
    return {}