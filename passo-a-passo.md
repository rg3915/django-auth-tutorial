
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

django-admin.py startproject myproject .
cd myproject
python ../manage.py startapp core
python ../manage.py startapp accounts

Edite `settings.py`

```python
# settings.py
import os
from decouple import config, Csv
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

