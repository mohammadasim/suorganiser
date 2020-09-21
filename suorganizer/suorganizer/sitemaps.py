"""
After creating the a Sitemap subclass for post.
We now create a sitemap dictionary. This is a
site-wide feature, so we create this module
and add PostSitemap to a dictionary.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from organizers.sitemaps import TagSitemap, StartupSitemap
from blogs.sitemaps import (PostSitemap, PostArchiveSitemap)


class RootSitemap(Sitemap):
    """
    Sitemap class for the
    root static pages such
    as about us etc.
    """
    priority = 0.6

    def items(self):
        """
        overriding the items method
        We return the url names of
        of our static page urls
        """
        return [
            'about_site',
            'site_mission',
            'site_work',
            'blogs_posts_list',
            'dj_auth:login',
            'organizers_startup_list',
            'organizers_tag_list',
        ]

    def location(self, url_name):
        """
        Method to create urls for
        the static pages.
        """
        return reverse(url_name)


sitemaps = {
    'post-archives': PostArchiveSitemap,
    'posts': PostSitemap,
    'roots': RootSitemap,
    'tags': TagSitemap,
    'startups': StartupSitemap,
}
