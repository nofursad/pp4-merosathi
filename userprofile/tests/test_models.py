from django.test import TestCase
from .models import Post, Comment


class TestPostModels(TestCase):

    # test that message value needs to be provided
    def test_message_is_required(self):
        form = CommentForm({'body': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors.keys())
        self.assertEqual(form.errors['body'][0], 'This field is required.')

    # test that message is named as an explicit field
    def test_fields_are_explicit_in_forms_metaclass(self):
        form = CommentForm()
        self.assertEqual(form.Meta.fields, ('body',))