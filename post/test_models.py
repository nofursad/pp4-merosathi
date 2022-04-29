from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment
from userprofile.models import Profile

User = get_user_model()

class TestPostModels(TestCase):
    # setup test data for post and comment
    def setUp(self):
        testuser = User.objects.create(username='testuser', email='test@user.com')
        testuser.is_staff = True
        testuser.is_superuser = True
        testuser.set_password('testpassword')
        self.post = Post.objects.create(
            content="This is test content",
            author=Profile.objects.create(user=testuser),
        )

    # test that message value needs to be provided
    def test_post_str(self):
        self.assertEqual(str(self.content), 'This is test content')

    # def test_total_likes(self):
    #     pass

    # def test_number_comments(Self):
    #     pass

    # def test_like_str(self):
    #     pass

