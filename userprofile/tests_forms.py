from django.test import TestCase
from .forms import CommentForm, PostForm


class TestCommentForm(TestCase):

    # test that message value needs to be provided
    def test_comment_is_required(self):
        form = CommentForm({'body': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors.keys())
        self.assertEqual(form.errors['body'][0], 'This field is required.')

    # test that message is named as an explicit field
    def test_fields_are_explicit_in_forms_metaclass(self):
        form = CommentForm()
        self.assertEqual(form.Meta.fields, ('body',))

class TestPostForm(TestCase):

    # test that message value needs to be provided
    def test_content_is_required(self):
        form = PostForm({'body': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors.keys())
        self.assertEqual(form.errors['content'][0], 'This field is required.')

    # test that message is named as an explicit field
    def test_fields_are_explicit_in_forms_metaclass(self):
        form = PostForm()
        self.assertEqual(form.Meta.fields, ('content', 'image'))