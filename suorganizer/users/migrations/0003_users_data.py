# Generated by Django 3.0.5 on 2020-08-21 04:47

from django.db import migrations
from django.contrib.auth.hashers import make_password

USERS = [
    {
        'email': 'ada@email.com',
        'password': 'myRandomString',
        'is_staff': False,
        'is_active': True,
        'is_superuser': False
    },
    {
        'email': 'dada@email.com',
        'password': 'myRandomString',
        'is_staff': True,
        'is_active': True,
        'is_superuser': True
    }
]


def add_user_data(apps, schema_editor):
    """
    Migration forward function to create
    users.
    ***Don't use in production.***
    :param apps:
    :param schema_editor:
    :return:
    """
    User = apps.get_model('users', 'User')
    for user in USERS:
        user_object = User.objects.create(
            email=user.get('email'),
            password=make_password(user.get('password')),
            is_staff=user.get('is_staff'),
            is_active=user.get('is_active'),
            is_superuser=user.get('is_superuser')
        )


def remove_user_data(apps, schema_editor):
    """
    Migration backward function to remove
    users.
    ***Don't use in production.***
    :param apps:
    :param schema_editor:
    :return:
    """
    User = apps.get_model('users', 'User')
    for user in USERS:
        user_object = User.objects.get(user['email'])
        user_object.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('blogs', '0005_posts_permissions'),
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.RunPython(
            add_user_data,
            remove_user_data
        )
    ]
