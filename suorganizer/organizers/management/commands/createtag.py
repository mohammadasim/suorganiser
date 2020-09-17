from django.core.management.base import (
    BaseCommand, CommandError
)
from django.utils.text import slugify

from ...models import Tag


class Command(BaseCommand):
    """
    Command class is required for create a
    custom management command
    """
    help = "Create new Tag."

    # First task is to tell the command what kind of
    # arguments it should expect.
    # The BaseCommand class expects us to define the
    # add_arguments() method, to which the command will
    # pass an ArgumentParser object.

    def add_arguments(self, parser):
        """
        Method that will receive the
        command line arguments passed
        by the user.
        This method will receive these
        arguments from the command class.
        :param parser:
        :return:
        """
        parser.add_argument(
            'tag_name',
            default=None,
            help='New tag name.'
        )

    # When the command is invoked it uses the handle()
    # method to use the expected arguments.

    def handle(self, *args, **options):
        """
        Method to execute the command
        i-e get the commandline arg
        and create the tag
        :param args:
        :param options:
        :return:
        """
        tag_name = options.pop('tag_name', None)
        Tag.objects.create(
            name=tag_name,
            slug=slugify(tag_name)
        )
