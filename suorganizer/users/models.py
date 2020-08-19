from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, )


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
    name = models.CharField(
        max_length=255
    )
    joined = models.DateTimeField(
        'Date Joined',
        auto_now_add=True
    )

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


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text=(
            'Designates whether the user can'
            'log into the admin site.'
        )
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should'
            'be treated as active. Unselect this'
            'instead of deleting accounts.'
        )
    )
    USERNAME_FIELD = 'email'

    def __str__(self):
        """
        Returns email of the user
        :return:
        """
        return self.email

    def get_absolute_url(self):
        """
        Returns user profile
        absolute url
        :return:
        """
        return self.profile.get_absolute_url()

    def get_full_name(self):
        """
        Returns profile name
        :return:
        """
        return self.profile.name

    def get_short_name(self):
        """
        Returns profile name
        :return:
        """
        return self.profile.name
