"""
Module to create superuser
"""
from django.core.management import CommandError
from django.utils.text import slugify
from users.models import Profile

from .createuser import Command as BaseCommand


class Command(BaseCommand):
    """
    Command class required for running
    management command. BaseCommand is
    imported from createuser to make
    use of the methods defined in that
    module
    """
    help = 'Create new Super User with Profile.'

    def create_user(self,
                    name, username, password):
        """
        Overriding the method in createuser
        to create superuser.
        :param name:
        :param username:
        :param password:
        :return:
        """
        new_user = (
            self.user.objects.create_superuser(
                email=username,
                password=password
            )
        )
        try:
            Profile.objects.create(
                user=new_user,
                name=name,
                slug=slugify(name)
            )

        except Exception as e:
            raise CommandError(
                'Could not create Profile:\n{}'
                    .format('; '.join(e.message))
            )
