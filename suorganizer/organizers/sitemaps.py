"""
Not every sitemap needs to be as complex as
the post sitmap. Django anticipates that in
most cases, we will simply override the
items() method of the Sitemap subclass and
nothing else. To make this easy the sitemaps
app supplies the GenericSitemap class, which
can be passed a dictionary of items to
automatically generate Sitemap subclass
"""

from django.contrib.sitemaps import (
    GenericSitemap, Sitemap
)
from .models import Tag, Startup

tag_sitemap_dict = {
    'queryset': Tag.objects.all(),
}
TagSitemap = GenericSitemap(tag_sitemap_dict)


class StartupSitemap(Sitemap):
    """
    Class for implementing sitemap
    functionality for Startup
    """
    model = Startup

    def items(self):
        """
        overriding the items method
        of the Sitemap class
        """
        return self.model.objects.all()

    def lastmod(self, startup):
        """
        If a startup has a newslink
        this method will calculate
        mod based on that, else it
        will be based on the founded_date
        """
        if startup.newslink_set.exists():
            return (
                startup.newslink_set.latest().pub_date
            )
        else:
            return startup.founded_date
