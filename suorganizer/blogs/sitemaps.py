from datetime import date
from itertools import chain
from math import log10
from operator import itemgetter

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


class PostSitemap(Sitemap):
    """
    Class to provide sitemap
    functionality for Post
    model
    """
    # The frequency with which the items
    # will change. In our case we have set
    # it to never.
    changefreq = 'never'
    priority = 0.5
    model = Post
    # attribute for priority
    period = 90

    def items(self):
        """
        Method to return
        all the published posts
        """
        return self.model.objects.published()

    def lastmod(self, post):
        """
        Method to return the
        last modified date of
        the post.
        """
        return post.pub_date

    """
    The priority attribute for each webpage
    is considered by some as the most important
    while by some as he least important.
    We will implement it here as an example for
    future reference.
    The integer 1 is given the most priority, 0
    is given none, while 0.5 is normal priority.
    """

    def priority(self, post):
        """
        Method to assign priority
        to each blog post
        1.0 is most important
        0.0 is least important
        0.5 is the default
        priority is assigned based
        on date. The most recent
        published post has the
        highest priority.
        """
        period = self.period  # 90 days
        timedelta = date.today() - post.pub_date
        # 86400 seconds in a day
        # 60 seconds * 60 minutes * 24 hours = 86400 seconds
        # we use floor division
        days = timedelta.total_seconds() // 86400
        if days == 0:
            return 1.0
        elif 0 < days <= period:
            # n(d) = normalized(days)
            # n(1) = 0.5
            # n(period) = 0
            normalized = (
                    log10(period / days) /
                    log10(period ** 2)
            )
            normalized = round(normalized, 2)
            return normalized + 0.5
        else:
            return 0.5


class PostArchiveSitemap(Sitemap):
    """
    For webpages that list post objects
    according to date we want to list
    pages for both the year and month
    archives and we want these pages
    to be sorted according to date, so
    that the month archives appear
    before the year archives (for the
    same year)
    """

    def items(self):
        """
        overriding items method.
        We get all the dates for the
        Post objects, first according
        to the year and then according
        to the month.
        We then add each date to a tuple
        noting which tuple was from
        year query and which was for month
        query.
        dates() method returns a QuerySet that
        evaluates to a list of datetime.date object
        representing all available dates of a
        particular kind within the contents of
        the queryset.
        iterator() evaluates the queryset and
        returns an iterator over the results.
        A queryset typically caches its results
        internally so that repeated evaluations
        do not result in additional queries.
        In contrast, iterator() will read results
        directly without doing any caching at the
        Queryset level. For queryset which returns
        a large number of objects that you only
        need to access once, this can result in
        better performance and a significant
        reduction in memory.
        """
        year_dates = (
            Post.objects.published().dates(
                'pub_date', 'year', order='DESC'
            ).iterator()
        )
        month_dates = (
            Post.objects.published().dates(
                'pub_date', 'month', order='DESC'
            ).iterator()
        )
        year_tuples = map(
            lambda d: (d, 'y'),
            year_dates
        )
        month_tuples = map(
            lambda d: (d, 'm'),
            month_dates
        )
        """
        To sort all dates together we use python's
        sorted() function, which notably respects place.
        We first use the chain() function to build a 
        single iterable from both tuples to sort through.
        Because sorted() is in place we pass the month 
        tuple to chain first(as we want the any month pages
        for a year to appear before the year page) We only
        want to sort the tuples according to the date, which
        is the first item in the tuple. We use the itemgtter()
        function to give sorted() that date from the tuple.
        Finally we want the latest dates first, so we ask for
        the reverse sort
        """
        return sorted(
            chain(month_tuples, year_tuples),
            key=itemgetter(0),
            reverse=True
        )

    def location(self, date_tuple):
        """
        In the previous Sitemap subclasses
        the links or locations for all of
        these pages were being created
        because we defined the get_absolute_url
        method on the models whose instance we
        were passing as items. In the case of
        our dates we don't have items, and so
        we need to implement the location method.
        """
        archive_date, archive_type = date_tuple
        if archive_type == 'y':
            return reverse(
                'blogs_post_archive_year',
                kwargs={
                    'year': archive_date.year
                }
            )
        elif  archive_type == 'm':
            return reverse(
                'blogs_post_archive_month',
                kwargs={
                    'year': archive_date.year,
                    'month': archive_date.month
                }
            )
        else:
            raise NotImplementedError(
                "{} did not recognize "
                "{} denoted '{}'".format(
                    self.__class__.__name__,
                    archive_type,
                    archive_type
                )
            )


