from django.test import TestCase
from .forms import ProfileModelForm


class TestProfileModelForm(TestCase):

    # test that message value needs to be provided
    def test_userdetail_is_required(self):
        form = ProfileModelForm({
            'first_name': '',
            'last_name': '',
            })
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors.keys())
        self.assertEqual(form.errors['first_name'][0], 'This field is required.')

    # test that message is named as an explicit field
    def test_fields_are_explicit_in_forms_metaclass(self):
        form = ProfileModelForm()
        self.assertEqual(form.Meta.fields, ('first_name','last_name'))
