"""suorganizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from blogs import urls as blog_urls
from contacts import urls as contact_urls
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.contrib.sitemaps.views import (
    index as site_index_view,
    sitemap as sitemap_view
)

from .sitemaps import sitemaps as sitemaps_dict
from organizers.urls import startup as start_urls
from organizers.urls import tag as tag_urls
from users import urls as user_urls
from blogs.feeds import AtomPostFeed, Rss2PostFeed
from organizers.feeds import AtomStartupFeed, Rss2StartupFeed

admin.site.site_header = 'Startup Organizer Admin'
admin.site.site_title = 'Startup Organizer Site Admin'
# Url configuration for new feeds
sitenews = [
    path('atom/', AtomPostFeed(), name='blogs_atom_feed'),
    path('rss/', Rss2PostFeed(), name='blogs_rss_feed'),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include(blog_urls)),
    path('contact/', include(contact_urls)),
    path('startup/', include(start_urls)),
    path('tag/', include(tag_urls)),
    path('about/', TemplateView.as_view(template_name='site/about.html'), name='about_site'),
    path('mission/', TemplateView.as_view(template_name='site/mission.html'), name='site_mission'),
    path('how/', TemplateView.as_view(template_name='site/work.html'), name='site_work'),
    path('', RedirectView.as_view(
        pattern_name='blogs_posts_list',
        permanent=False
    )),
    path('users/', include(user_urls,
                           namespace='dj-auth')),
    path('sitenews/', include(sitenews)),
    path('<slug:startup_slug>/atom/', AtomStartupFeed(), name='organizers_startup_atom_feed'),
    path('<slug:startup_slug>/rss/', Rss2StartupFeed(), name='organizers_startup_rss_feed'),
    # The index view is a higher level overview of the sitemaps
    # for each section of the application.
    path('sitemap.xml', site_index_view, {'sitemaps': sitemaps_dict},
         name='sitemaps'),
    path('sitemap-<section>.xml', sitemap_view, {'sitemaps': sitemaps_dict},
         name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
