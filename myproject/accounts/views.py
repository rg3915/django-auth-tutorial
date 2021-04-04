from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from myproject.accounts.forms import SignupForm


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
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
