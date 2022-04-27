from django.test import TestCase
from .models import Post, Comment


class TestPostModels(TestCase):

    # setup test data for post and comment
    def test_data(self):
        self.post = Post.objects.create{
            content="This is test content"
            image=""
            liked="abhisek"
            updated_on=""
            created_on=""
            author="abhisek"
        }

    # test that message value needs to be provided
    def test_model_str(self):
        self.assertEqual(str(self.post), 'This is test content')
