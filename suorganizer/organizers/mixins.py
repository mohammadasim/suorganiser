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


class PageLinksMixin:
    """
    A class to create pagination urls
    """
    page_kwarg = 'page'

    def _page_urls(self, page_number):
        """
        A method to create a pagination url with
        the value of queryset page to to the page_number
        :param page_number:
        :return: url(string)
        """
        return '?{pkw}={n}'.format(
            pkw=self.page_kwarg,
            n=page_number
        )

    def previous_page(self, page):
        """
        A method to return the previous page url
        :param page:
        :return:
        """
        if page.has_previous():
            return self._page_urls(page.previous_page_number())
        return None

    def next_page(self, page):
        if page.has_next():
            return self._page_urls(page.next_page_number())
        return None

    def get_context_data(self, **kwargs):
        """
        Overriding method to add data for previous and next pages
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        page = context.get('page_obj')
        if page is not None:
            context.update({
                'previous_page_url':
                    self.previous_page(page),
                'next_page_url':
                    self.next_page(page)
            })
        return context
