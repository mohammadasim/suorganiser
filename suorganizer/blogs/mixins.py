from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.dates import (
    YearMixin as BaseYearMixin, MonthMixin as BaseMonthMixin,
    DateMixin, _date_from_string)

from .models import Post


class AllowFuturePermissionMixin:
    """
    Mixin to check if user has
    'blog.view_future_post' permission
    """

    def get_allow_future(self):
        """
        if user has the permission returns true
        else returns false
        :return:
        """
        return self.request.user.has_perm(
            'blog.view_future_post')


class MonthMixin(BaseMonthMixin):
    """
    This class overrides the django monthmixin to add
    extra functionalities defined in yearmixin class.
    """
    month_format = '%m'
    month_query_kwarg = 'month'
    month_url_kwarg = 'month'

    def get_month(self):
        month = self.month
        if month is None:
            month = self.kwargs.get(
                self.month_url_kwarg,
                self.request.GET.get(
                    self.month_query_kwarg
                )
            )
        if month is None:
            raise Http404("No month specified")
        return month


class YearMixin(BaseYearMixin):
    """
    Django's yearmixin forces us to define year in the url pattern only
    and call it 'year'. In this class we have modified that behaviour
    the year can be defined as an attribute in the subclass of this class.
    The year can be called anything in the url patten by overriding the 'year_url_kwarg'
    attribute. The year can be called anything and set as part of query, by overriding
    'year_query_kwarg'.
    """
    year_query_kwarg = 'year'
    year_url_kwarg = 'year'

    def get_year(self):
        year = self.year
        if year is None:
            year = self.kwargs.get(
                self.year_url_kwarg,
                self.request.GET.get(
                    self.year_query_kwarg
                )
            )
        if year is None:
            raise Http404("No year specified")
        return year


class DateObjectMixin(YearMixin,
                      MonthMixin,
                      DateMixin,
                      AllowFuturePermissionMixin):

    def get_object(self, queryset=None):
        """
        In this method django builds the keyword arguments for
        the query(to find the object in the database)
        The method creates the date kwargs for queryset and then pass
        that query set to the super queryset that contains the slug.
        :param queryset:
        :return:
        """
        year = self.get_year()
        month = self.get_month()
        date = _date_from_string(
            year, self.get_year_format(),
            month, self.get_month_format()
        )
        if queryset is None:
            queryset = self.get_queryset()

        if (not self.allow_future
                and date > date.today()):
            raise Http404(
                'Future {} not available because'
                '{}. allow_future is False'.format(
                    queryset.model._meta.verbose_name_plural,
                    self.__class__.__name__
                )
            )
        filter_dict = (
            self._make_single_date_lookup(date)
        )
        queryset = queryset.filter(**filter_dict)
        return super().get_object(queryset=queryset)

    def _make_single_date_lookup(self, date):
        """
        In this method we add timezone to the date if
        the date_field as DateTimeField in the model.
        If the date_field is set to datefield we simply use
        _get_next_month() to setup the range for query.
        :param date:
        :return:
        """
        date_field = self.get_date_field()
        if self.uses_datetime_field:
            since = self._make_date_lookup_arg(date)
            until = self._make_date_lookup_arg(self._get_next_month(date))
            return {
                '{}__gte'.format(date_field): since,
                '{}__lt'.format(date_field): until,
            }
        else:
            return {
                '{}__gte'.format(date_field): date,
                '{}__lt'.format(date_field): self._get_next_month(date),
            }


class PostFormValidMixin:
    """
    Mixin to override the
    form_valid method
    """

    def form_valid(self, form):
        """
        Overriding the method to
        pass request object to the
        form. This method is called
        when form is bound and valid.
        :param form:
        :return:
        """
        self.object = form.save(self.request)
        return HttpResponseRedirect(
            self.get_success_url()
        )


class BasePostFeedMixin:
    """
    Class implementing attributes
    and methods required for RSS
    and Atom Feeds.
    While both RSS and Atom feeds
    typically print the same
    information, Django will expect
    that we use different attributes
    and methods for each one, despite
    the fact that they frequently
    serve the same purpose.
    In case of description attribute,
    description is for RSS and
    subtitle is for Atom feed.
    """
    title = 'Latest Startup Organizer Blog Posts'
    link = reverse_lazy('blogs_posts_list')
    description = subtitle = (
        'Stay up to date on the '
        'hottest startup news.'
    )

    def items(self):
        """
        Method to provide the
        list of items listed
        in the feed.
        This method will be
        used by both RSS and
        Atom.
        """
        # uses Post.Meta.ordering
        return Post.objects.published()[:10]

    def item_title(self, item):
        """
        Method that returns the
        formatted title
        of the item provided in
        the args.
        """
        return item.formatted_title()

    def item_description(self, item):
        """
        Method that returns a short
        description of the item
        provided in the argument.
        """
        return item.short_text()

    def item_link(self, item):
        """
        Method that returns
        the link for item
        provided in the args.
        """
        return item.get_absolute_url()
