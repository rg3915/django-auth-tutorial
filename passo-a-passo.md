
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

django-admin.py startproject myproject .
cd myproject
python ../manage.py startapp core
python ../manage.py startapp accounts
python contrib/env_gen.py


Edite `settings.py`

```python
# settings.py
import os

from decouple import Csv, config
from dj_database_url import parse as dburl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

# Application definition

INSTALLED_APPS = [
    ...
    'django_extensions',
    'myproject.accounts',
    'myproject.core',
]

default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
}


LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

...

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:index'
LOGOUT_REDIRECT_URL = 'core:index'
```

python manage.py migrate

Criando algumas pastas

mkdir -p myproject/core/templates
mkdir -p myproject/core/static/css

mkdir -p myproject/accounts/templates/{accounts,email,registration}


Criando alguns arquivos

touch myproject/core/templates/{base,index,nav}.html
touch myproject/core/static/css/{style,login}.css
touch myproject/core/urls.py
touch myproject/accounts/urls.py


Editando base.html
Editando index.html
Editando nav.html
Editando style.css
Editando urls.py
Editando core/urls.py
Editando core/views.py

Editando accounts/urls.py

O template padrão é `registration/login.html`, mas vamos mudar

```python
from django.contrib.auth.views import LoginView
# accounts/urls.py
from django.urls import path

app_name = 'accounts'


urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
]
```

Editando accounts/login.html

touch myproject/accounts/templates/accounts/login.html

A partir de https://github.com/rg3915/coreui-django-boilerplate-v2/blob/main/myproject/core/templates/login.html

Editando accounts/signup.html


Editando accounts/urls.py

from myproject.accounts.views import signup

    path('signup/', signup, name='signup'),


Editando accounts/views.py


Editando accounts/forms.py

touch myproject/accounts/forms.py


Editando accounts/templates/accounts/signup.html

touch myproject/accounts/templates/accounts/signup.html


A partir de https://github.com/rg3915/coreui-django-boilerplate-v2/blob/main/myproject/core/templates/register.html

