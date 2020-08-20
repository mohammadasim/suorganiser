from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)


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
        return self.user.get_full_name()

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


class UserManager(BaseUserManager):
    """
    Custom manager for the custom User model
    """
    use_in_migrations = True

    def _create_user(self,
                     email, password, **kwargs):
        """
        Private method to create and save
        a user with the given username, email,
        and password.
        :param email:
        :param password:
        :param kwargs:
        :return:
        """
        # Normalize the email address by lowercasing the domain part of it.
        email = self.normalize_email(email)
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop(
            'is_superuser', False)
        user = self.model(
            email=email,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,
                    email, password=None, **extra_fields):
        """
        Public method for creating user
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self,
                         email, password, **extra_fields):
        """
        Method to create super user
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        return self._create_user(
            email,
            password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text=(
            'Designates whether the user can '
            'log into the admin site.'
        )
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should '
            'be treated as active. Unselect this '
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
        We are using the 1to1 relationship
        :return:
        """
        return self.profile.name

    def get_short_name(self):
        """
        Returns profile name
        We are using the 1to1 relationship
        :return:
        """
        return self.profile.name

    # overriding objects attribute to use
    # the custom manager that we have created
    objects = UserManager()
