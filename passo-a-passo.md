# Passo a passo

```
git clone https://github.com/rg3915/django-auth-tutorial.git
cd django-auth-tutorial
git branch base origin/base
git checkout base

python3 -m venv .venv
source .venv/bin/activate

# Django==3.1.8 django-utils-six django-extensions python-decouple
cat requirements.txt

pip install -U pip
pip install -r requirements.txt
pip install ipdb

python contrib/env_gen.py

python manage.py migrate
python manage.py createsuperuser --username="admin" --email="admin@email.com"

python manage.py shell_plus
```

https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.UserManager.create_user


```python
python manage.py shell_plus

from django.contrib.auth.models import User

user = User.objects.create_user(
    username='regis', 
    email='regis@email.com', 
    password='demodemo',
    first_name='Regis',
    last_name='Santos',
    is_active=True
)
```

```
cat myproject/settings.py
```


```python
INSTALLED_APPS = [
    'myproject.accounts',  # <---
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    'django_extensions',
    'widget_tweaks',
    'myproject.core',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
EMAIL_HOST = config('EMAIL_HOST', '0.0.0.0')  # localhost
EMAIL_PORT = config('EMAIL_PORT', 1025, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)


LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'core:index'
LOGOUT_REDIRECT_URL = 'core:index'
```

Estrutura do projeto

```
tree
```

Agora veja as imagens em [README.md](README.md).

Criando alguns arquivos

```
touch myproject/core/urls.py
touch myproject/accounts/urls.py
```



Editando `urls.py`

```python
# urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('myproject.core.urls', namespace='core')),
    # 
    path('accounts/', include('myproject.accounts.urls')),  # sem namespace
    path('admin/', admin.site.urls),
]
```

Editando `core/urls.py`

```
touch myproject/core/urls.py
```


```python
# core/urls.py
from django.urls import path

from myproject.core import views as v

app_name = 'core'


urlpatterns = [
    path('', v.index, name='index'),
]
```

Editando `core/views.py`

```python
# core/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    template_name = 'index.html'
    return render(request, template_name)
```

Editando `accounts/urls.py`

```
touch myproject/accounts/urls.py
```

O template padrão é `registration/login.html`, mas vamos mudar

```python
# accounts/urls.py
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
    path('logout/', LogoutView.as_view(), name='logout'),
]
```


Editando accounts/urls.py

```python
# accounts/urls.py
    ...
    path('signup/', v.signup, name='signup'),
    # path('signup/', v.SignUpView.as_view(), name='signup'),
    path('signup-email/', v.signup_email, name='signup_email'),
    path(
        'account-activation-done/',
        v.account_activation_done,
        name='account_activation_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        v.MyPasswordResetConfirm.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        v.MyPasswordResetComplete.as_view(),
        name='password_reset_complete'
    ),
    ...
```

Editando accounts/tokens.py

```python
# accounts/tokens.py
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
        )


account_activation_token = AccountActivationTokenGenerator()
```


Editando accounts/views.py

```python
# accounts/views.py
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
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


def send_mail_to_user(request, user):
    current_site = get_current_site(request)
    use_https = request.is_secure()
    subject = 'Ative sua conta.'
    message = render_to_string('email/account_activation_email.html', {
        'user': user,
        'protocol': 'https' if use_https else 'http',
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)


def signup_email(request):
    form = SignupEmailForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_mail_to_user(request, user)
            return redirect('account_activation_done')

    return render(request, 'accounts/signup_email_form.html', context)


def account_activation_done(request):
    return render(request, 'accounts/account_activation_done.html')


class MyPasswordResetConfirm(PasswordResetConfirmView):

    def form_valid(self, form):
        self.user.is_active = True
        self.user.save()
        return super(MyPasswordResetConfirm, self).form_valid(form)


class MyPasswordResetComplete(PasswordResetCompleteView):
    ...
```

Editando `accounts/forms.py`

```
touch myproject/accounts/forms.py
```

```python
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from myproject.accounts.models import UserProfile


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'})
    )
    last_name = forms.CharField(label='Sobrenome', max_length=30, required=False)  # noqa E501
    username = forms.CharField(label='Usuário', max_length=150)
    email = forms.CharField(
        label='E-mail',
        max_length=254,
        help_text='Requerido. Informe um e-mail válido.',
    )
    # cpf = forms.CharField(label='CPF')

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        )


class SignupEmailForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'})
    )
    last_name = forms.CharField(label='Sobrenome', max_length=30, required=False)  # noqa E501
    username = forms.CharField(label='Usuário', max_length=150)
    email = forms.CharField(
        label='E-mail',
        max_length=254,
        help_text='Requerido. Informe um e-mail válido.',
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
        )
```



Em accounts/views.py

```python
# accounts/views.py
class MyPasswordChange(PasswordChangeView):
    ...


class MyPasswordChangeDone(PasswordChangeDoneView):

    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy('login'))
```

Em accounts/urls.py

```python
# accounts/urls.py
    ...
    path(
        'password_change/',
        v.MyPasswordChange.as_view(),
        name='password_change'
    ),
    path(
        'password_change/done/',
        v.MyPasswordChangeDone.as_view(),
        name='password_change_done'
    ),
    ...
```

Em accounts/views.py

```python
# accounts/views.py

# Requer
# registration/password_reset_email.html
# registration/password_reset_subject.txt
class MyPasswordReset(PasswordResetView):
    ...


class MyPasswordResetDone(PasswordResetDoneView):
    ...


class MyPasswordResetConfirm(PasswordResetConfirmView):

    def form_valid(self, form):
        self.user.is_active = True
        self.user.save()
        return super(MyPasswordResetConfirm, self).form_valid(form)


class MyPasswordResetComplete(PasswordResetCompleteView):
    ...

```

Em accounts/urls.py

```python
# accounts/urls.py
    ...
    path(
        'password_reset/',
        v.MyPasswordReset.as_view(),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        v.MyPasswordResetDone.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        v.MyPasswordResetConfirm.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        v.MyPasswordResetComplete.as_view(),
        name='password_reset_complete'
    ),
    ...
```

---

Falar de `include('django.contrib.auth.urls')` include em `urls.py`

```python
# urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),  # sem namespace
]
```
