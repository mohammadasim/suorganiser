"""
Utility module for organizers app
"""
from django.forms import forms
from django.shortcuts import get_object_or_404

from .models import Startup, NewsLink


class SlugCleanMixin:
    """
    Mixin class for slug cleaning method
    """

    def clean_slug(self):
        """
        Method to check if slug is called create
        :return:
        """
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise forms.ValidationError('Slug may not be "create".')
        return new_slug


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
        """
        A method to return the next page url
        :param page:
        :return:
        """
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


class StartupContextMixin:
    """
    A mixin class to get startup object and
    add it to the context. All newslink views will
    inherit this class and their context objects
    will have a startup object
    """
    startup_slug_url_kwarg = 'startup_slug'
    startup_context_object_name = 'startup'

    def get_context_data(self, **kwargs):
        """
        Overriding the method to add
        startup to the context object
        :param kwargs:
        :return:
        """
        if hasattr(self, 'startup'):
            context = {
                self.startup_context_object_name:
                    self.startup
            }
        else:
            startup_slug = self.kwargs.get(
                self.startup_slug_url_kwarg
            )
            startup = get_object_or_404(
                Startup, slug__iexact=startup_slug
            )
            context = {
                self.startup_context_object_name:
                    startup
            }
        # Add the kwargs to the context object just created
        context.update(kwargs)
        return super().get_context_data(**context)


class NewsLinkGetObjectMixin:
    """
    Class to override the get_object()
    to ensure that the correct newslink object
    is retrieved as newslink objects are unique
    based on startup slug and newslink slug
    """
    startup_slug_url_kwarg = 'startup_slug'
    newslink_slug_url_kwarg = 'newslink_slug'

    def get_object(self, queryset=None):
        """
        Overriding get_object method
        :param queryset:
        :return:
        """
        startup_slug = self.kwargs.get(
            self.startup_slug_url_kwarg
        )
        newslink_slug = self.kwargs.get(
            self.newslink_slug_url_kwarg
        )
        return get_object_or_404(
            NewsLink,
            slug__iexact=newslink_slug,
            startup__slug__iexact=startup_slug
        )


class BaseStartupFeedMixin:
    """
    Class to implement methods
    and attributes required for
    Atom and RSS feeds for
    Startup.
    As this feed is for a single
    object. We need to get that
    object.
    We therefore override the
    get_object(), this method
    is not like the get_object()
    found in GCBV, but is more
    like get() found in CBV.
    """
    def get_object(self, request, startup_slug):
        return get_object_or_404(
            Startup,
            slug__iexact=startup_slug
        )

    """
    When provided an object, the Feed class
    will pass the object to the items() method,
    allowing us to use Startup instance in the
    method to get the related NewsLink objects
    """

    def items(self, startup):
        return startup.newslink_set.all()[:10]

    """
    The item retrieved by items method is
    the newslink, so we define methods
    to get attributes of each newslink
    """

    def item_description(self, newslink):
        """
        Method that returns description
        of the newslink item retrieved
        by items method
        """
        return newslink.description()

    def item_link(self, newslink):
        """
        Method that returns link
        of the newslink item retrieved
        by the items method
        """
        return newslink.link

    def item_title(self, newslink):
        """
        Method that returns title of
        the newslink item returned
        by the items method
        """
        return newslink.title

    def description(self, startup):
        """
        Method that returns the
        description of startup
        that this feed is for.
        """
        return 'News related to {}'.format(
            startup.name
        )

    def link(self, startup):
        """
        Method to return the
        url for the startup
        detail page of the
        startup.
        """
        return startup.get_absolute_url()

    def subtitle(self, startup):
        """
        Method to return the description
        of the Startup. We have to define
        a subtitle method even though the
        description method is already there,
        because django wants subtitle method
        for Atom feed, while the description
        method is used by RSS Feed.
        """
        return self.description(startup)

    def title(self, startup):
        """
        Method to return the name
        of a startup.
        """
        return startup.name
