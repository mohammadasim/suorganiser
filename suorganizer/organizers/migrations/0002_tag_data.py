# Generated by Django 3.0.5 on 2020-04-21 07:03

from django.db import migrations

TAGS = (
    ('augmented reality', 'augmented-reality'),
    ('terraform automation', 'terraform-automation'),
    ('jenkins pipeline', 'jenkins-pipeline'),
    ('devops culture', 'devops-culture')
)


def add_tag_data(apps, schema_editor):
    Tag = apps.get_model('organizers', 'Tag')
    for tag_name, tag_slug in TAGS:
        Tag.objects.create(
            name=tag_name,
            slug=tag_slug
        )


def remove_tag_data(apps, schema_editor):
    Tag = apps.get_model('organizers', 'Tag')
    for _, tag_slug in TAGS:
        tag = Tag.objects.get(slug=tag_slug)
        tag.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('organizers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_tag_data,
            remove_tag_data
        )
    ]