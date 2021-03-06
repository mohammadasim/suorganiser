# Generated by Django 3.1.1 on 2020-09-16 06:13
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings


def add_site_data(apps, schema_editor):
    """
    function to add site data during
    migration
    """
    Site = apps.get_model('sites', 'Site')
    new_domain = 'site.django-unleashed.com'
    new_name = 'Startup Organizer'
    site_id = getattr(settings, 'SITE_ID', 1)
    # If there is a site, update its details
    if Site.objects.exists():
        current_site = Site.objects.get(pk=site_id)
        current_site.domain = new_domain
        current_site.name = new_name
        current_site.save()
    else:
        current_site = Site(
            pk=site_id,
            domain=new_domain,
            name=new_name
        )
        current_site.save()


def remove_site_data(apps, schema_editor):
    """
    function to remove the site data and
    set it back to example.com
    """
    Site = apps.get_model('sites', 'Site')
    current_site = Site.objects.get(
        pk=getattr(settings, 'SITE_ID', 1)
    )
    current_site.domain = 'example.com'
    current_site.name = 'example.com'
    current_site.save()


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.RunPython(add_site_data, remove_site_data,),
    ]
