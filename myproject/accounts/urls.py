from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from myproject.accounts import views as v

app_name = 'accounts'


urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', v.signup, name='signup'),
    # path('signup/', v.SignUpView.as_view(), name='signup'),
    path('signup-email/', v.signup_email, name='signup_email'),
    path(
        'account-activation-sent/',
        v.account_activation_sent,
        name='account_activation_sent'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        v.PasswordResetComplete.as_view(),
        name='password_reset_complete'
    ),
]
