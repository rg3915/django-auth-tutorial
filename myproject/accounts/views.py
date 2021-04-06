from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetView
)
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView

from myproject.accounts.forms import SignupEmailForm, SignupForm
from myproject.accounts.tokens import account_activation_token


def signup(request):
    form = SignupForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # Autentica usuário
            user = authenticate(username=username, password=raw_password)

            # Faz login
            auth_login(request, user)
            return redirect(reverse_lazy('core:index'))

    return render(request, 'accounts/signup.html', context)


class SignUpView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


def signup_email(request):
    form = SignupEmailForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Ative sua conta.'
            message = render_to_string('email/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')

    return render(request, 'accounts/signup_email.html', context)


def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
