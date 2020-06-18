"""
View Module for Users app
"""
from django.conf import settings
from django.contrib.auth import get_user, logout
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views import View


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
