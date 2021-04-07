from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from myproject.accounts import views as v

# Se usar app_name vai dar erro de redirect em PasswordResetView.
# app_name = 'accounts'


urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    # Se vc importou django.contrib.auth.urls em urls.py então não precisa do logout abaixo.  # noqa E501
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
        v.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        v.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path(
        'password_reset/',
        v.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        v.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
]
