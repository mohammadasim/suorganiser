"""
View Module for Users app
"""
from django.conf import settings
from django.contrib.auth import get_user, logout, get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.messages import error, success
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from .forms import UserCreationForm
from .mixins import MailContextViewMixin


class DisableAccount(LoginRequiredMixin, View):
    """
    A class to define view to disable user account
    """
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = (
        'users/user_confirm_delete.html'
    )

    def get(self, request):
        """GET Method"""
        return TemplateResponse(request, self.template_name)

    def post(self, request):
        """
        Disables the user account once user has confirmed it
        :param request:
        :return:
        """
        user = get_user(request)
        user.set_unusable_password()
        user.is_active = False
        user.save()
        logout(request)
        return redirect(self.success_url)


class CreateAccount(MailContextViewMixin, View):
    """
    A class view to create a user
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('dj-auth:create_done')
    template_name = 'users/user_create.html'

    def get(self, request):
        """
        Method to show form
        :return:
        """
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()}
        )

    @sensitive_post_parameters('password1', 'password2')
    def post(self, request):
        """
        Post method dealing with form once
        returned by the user
        :param request:
        :return:
        """
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            # we are using get_save_kwargs to get data from
            # request and pass it on to the save() that will
            # pass it to the send_mail method
            bound_form.save(self.get_save_kwargs(request))
            # using mail_sent from mixin we check if email
            # has been sent
            if bound_form.mail_sent:
                return redirect(self.success_url)
            else:
                errs = (
                    bound_form.non_field_errors()
                )
                for err in errs:
                    error(request, err)
        return TemplateResponse(request,
                                self.template_name,
                                {'form': bound_form})


class ActivateAccount(View):
    """
    View for dealing with activating
    account
    """
    success_url = reverse_lazy('dj-auth:login')
    template_name = 'users/user_active.html'

    @never_cache
    def get(self, request, uidb64, token):
        """
        Get method to check user using uidb64
        check that token is valid
        :param request:
        :param uidb64:
        :param token:
        :return:
        """
        user = get_user_model()
        try:
            uid = force_str(
                urlsafe_base64_decode(uidb64)
            )
            user = user.objects.get(pk=uid)
        except (TypeError, ValueError,
                OverflowError, user.DoesNotExist):
            user = None
        if user is not None and token_generator.check_token(token, user):
            user.is_active = True
            user.save()
            success(
                request,
                'User Activated!'
                'You may login.'
            )
            return redirect(self.success_url)
        else:
            return TemplateResponse(request,
                                    self.template_name)
