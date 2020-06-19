from django.contrib.auth import get_user_model
from django.contrib.auth.forms import \
    UserCreationForm as BaseUserCreationForm

from .mixins import ActivationMailFormMixin


class UserCreationForm(ActivationMailFormMixin,
                       BaseUserCreationForm):
    """
    Form class for user creation
    """
    mail_validation_error = (
        'User created. Could not send activation '
        'email. Please try again later. (Sorry!)'
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
        if send_mail:
            self.send_mail(**kwargs)
        return user

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
        fields = ['username', 'email']
