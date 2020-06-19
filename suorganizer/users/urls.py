from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView, TemplateView

from .views import DisableAccount, CreateAccount, ActivateAccount

app_name = 'dj-auth'

password_url = [
    path('change/',
         auth_views.PasswordChangeView.as_view(
             template_name='users/password_change_form.html',
             success_url=reverse_lazy('dj-auth:pw_change_done')
         ), name='pw_change'),
    path('change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'
         ), name='pw_change_done'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.txt',
        subject_template_name='users/password_reset_subject.txt',
        success_url=reverse_lazy('dj-auth:pw_reset_sent')
    ), name='pw_reset_start'),
    path('reset/sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_sent.html'
    ), name='pw_reset_sent'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('dj-auth:pw_reset_complete')
    ), name='pw_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html',
        extra_context={'form': 'AuthenticationForm'}
    ), name='pw_reset_complete')

]

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'
    )
         , name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logged_out.html',
        extra_context={
            'form': AuthenticationForm
        }
    )
         , name='logout'),
    path('', RedirectView.as_view(
        pattern_name='dj-auth:login',
        permanent=False
    ), ),
    path('password/', include(password_url)),
    path('disable/', DisableAccount.as_view(), name='disable'),
    path('create/', CreateAccount.as_view(), name='create'),
    path('create/done/', TemplateView.as_view(
        template_name='users/user_create_done.html'),
         name='create_done'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(),
         name='activate'),
]
