from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from django.views.generic import RedirectView

app_name = 'dj-auth'

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
    ), )
]
