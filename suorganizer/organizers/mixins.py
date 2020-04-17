from django.forms import forms


class SlugCleanMixin:
    """
    Mixin class for slug cleaning method
    """

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise forms.ValidationError('Slug may not be "create".')
        return new_slug
