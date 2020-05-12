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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include('blogs.urls')),
    path('contact/', include('contacts.urls')),
    path('newslink/', include('organizers.urls.newslink')),
    path('startup/', include('organizers.urls.startup')),
    path('tag/', include('organizers.urls.tag')),
    path('about/', TemplateView.as_view(template_name='site/about.html'), name='about_site'),
    path('mission/', TemplateView.as_view(template_name='site/mission.html'), name='site_mission'),
    path('how/', TemplateView.as_view(template_name='site/work.html'), name='site_work'),
    path('', RedirectView.as_view(
        pattern_name='blogs_posts_list',
        permanent=False
    ))
]
