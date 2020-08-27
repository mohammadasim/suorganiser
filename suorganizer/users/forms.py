import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import \
    UserCreationForm as BaseUserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .mixins import ActivationMailFormMixin
from .models import Profile

logger = logging.getLogger(__name__)


class UserCreationForm(ActivationMailFormMixin,
                       BaseUserCreationForm):
    """
    Form class for user creation
    """
    mail_validation_error = (
        'User created. Could not send activation '
        'email. Please try again later. (Sorry!)'
    )
    # Name field added to the form only.
    # The value from this field will be used
    # to create profile for the user
    name = forms.CharField(
        max_length=255,
        help_text=(
            'The name displayed on your '
            'public profile.'
        )
    )

    def save(self, **kwargs):
        """
        Overriding save method with multiple steps
        Passing it **kwargs required by send_mail()
        We then get the user and check if it already
        has a primary key in the database, if it has
        it means the user data is already in the database
        and we don't need to send an account activation
        email, if the primary key is not in the database
        we then send the account activation email.
        :param kwargs:
        :return:
        """
        user = super().save(commit=False)
        if not user.pk:
            user.is_active = False
            send_mail = True
        else:
            send_mail = False
        # After knowing to send email or not we need to save
        # the user to the database.
        user.save()
        # To save any many-to-many relations we call save_m2m()
        self.save_m2m
        # create or update the user profile
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'name': self.cleaned_data['name'],
                'slug': slugify(self.cleaned_data['name'])
            }
        )
        if send_mail:
            self.send_mail(user, **kwargs)
        return user

    def clean_name(self):
        """
        Method to check that name is
        not in the set of disallowed
        names. If name of user is
        login it means their profile will
        be accessible with url users/login/
        which is our login url.
        :return:
        """
        name = self.cleaned_data['name']
        disallowed = (
            'activate',
            'create',
            'disable',
            'login',
            'logout',
            'password',
            'profile',
        )
        if name in disallowed:
            raise ValidationError(
                'A user with that username'
                'already exists.'
            )
        return name

    class Meta(BaseUserCreationForm.Meta):
        """
        To properly restructure UserCreationForm to use
        the fields in BaseUserCreationForm, we need to
        change the Meta class where the ModelForm
        behaviour is defined.
        This meta class therefore inherits the Meta class
        in BaseUserCreationForm, overriding the model
        with get_user_model() and adding the email
        form to the field.
        """
        model = get_user_model()
        fields = ['email', 'email']


class ResendActivationEmailForm(ActivationMailFormMixin,
                                forms.Form):
    """
    Form class for sending activation link to user
    whose previous link has expired.
    """

    email = forms.EmailField()

    mail_validation_error = (
        'Could not re-send activation email.'
        'Please try again later.'
    )

    def save(self, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(
                email=self.cleaned_data['email']
            )
        except:
            logger.warning(
                'Resend Activation: No user with'
                'email: {} .'.format(self.cleaned_data['email'])
            )
            return None
        self.send_mail(user=user, **kwargs)
        return user
