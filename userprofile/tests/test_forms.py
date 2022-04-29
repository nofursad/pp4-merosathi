from django.test import TestCase
from .forms import ProfileModelForm


class TestProfileModelForm(TestCase):

    # test that field is named as an explicit field
    def test_fields_are_explicit_in_forms_metaclass(self):
        form = ProfileModelForm()
        self.assertEqual(form.Meta.fields, (
            'first_name',
            'last_name',
            'bio',
            'avatar',
            ))
