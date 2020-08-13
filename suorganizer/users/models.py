from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    A model representing a user profile
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True
    )
    slug = models.SlugField(
        max_length=30,
        unique=True
    )
    about = models.TextField()

    def __str__(self):
        return self.user.get_username()

