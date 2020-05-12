from django.forms import forms
from django.urls import reverse


class SlugCleanMixin:
    """
    Mixin class for slug cleaning method
    """

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise forms.ValidationError('Slug may not be "create".')
        return new_slug


class ObjectPaginateMixin:
    reverse_url_name = ''

    def get_next_url(self, page):
        if page.has_next():
            return reverse(
                self.reverse_url_name,
                args=(
                    page.next_page_number(),
                )
            )
        else:
            return None

    def get_previous_url(self, page):
        if page.has_previous():
            return reverse(
                self.reverse_url_name,
                args=(
                    page.previous_page_number(),
                )
            )
        else:
            return None
