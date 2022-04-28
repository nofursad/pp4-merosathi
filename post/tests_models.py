from django.test import TestCase
from .models import Post, Comment, Profile


class TestPostModels(TestCase):

    # setup test data for post and comment
    def test_data(self):
        self.user = Profile.objects.create(user='testuser')

        self.post = Post.objects.create(
            content="This is test content",
            author=self.user
        )

        self.comment = Comment.objects.create(
            # user=self.user,
            post=self.post,
            body='this is comment for test content'
        )

    # test that message value needs to be provided
    def test_model_str(self):
        self.assertEqual(str(self.post), 'This is test content')
