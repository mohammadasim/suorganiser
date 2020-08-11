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

