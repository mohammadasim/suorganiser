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
