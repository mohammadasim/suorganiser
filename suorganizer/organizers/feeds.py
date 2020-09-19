from datetime import datetime

from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import (
    Atom1Feed, Rss201rev2Feed
)

from .mixins import BaseStartupFeedMixin


class AtomStartupFeed(BaseStartupFeedMixin, Feed):
    """
    Class for generating Atom feeds for
    Startup model
    """
    feed_type = Atom1Feed


class Rss2StartupFeed(BaseStartupFeedMixin, Feed):
    """
    class for generating RSS feed for
    Startup model
    """
    feed_type = Rss201rev2Feed
