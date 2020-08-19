from django.conf import settings
from django.db import models
from django.urls import reverse


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

    def get_update_url(self):
        """
        Method to return the profile
        update url
        :return:
        """
        return reverse('dj-auth:profile_update')

    def get_absolute_url(self):
        """
        Method to return absolute url
        for profile
        :return:
        """
        return reverse('dj-auth:public_profile',
                       kwargs={'slug': self.slug})

