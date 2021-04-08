# Guia de autenticação com Django

## Este projeto foi feito com:

* [Python 3.8.2](https://www.python.org/)
* [Django 3.1.7](https://www.djangoproject.com/)
* [Bootstrap 4.0](https://getbootstrap.com/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/django-auth-tutorial.git
cd django-auth-tutorial
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
python manage.py createsuperuser --username='admin' --email=''
```

## Estrutura

### Login

![101_login_logout.png](img/101_login_logout.png)

### Cadastro

![102_signup.png](img/102_signup.png)

### Trocar senha

![103_change_password.png](img/103_change_password.png)

### Esqueci minha senha

![104_reset_password.png](img/104_reset_password.png)



## Telas

### Login

![01_login.png](img/01_login.png)

### Cadastro

![02_signup.png](img/02_signup.png)

### Trocar senha

![03_change_password.png](img/03_change_password.png)

### Esqueci minha senha

![04_forgot_password.png](img/04_forgot_password.png)


## Links

https://docs.djangoproject.com/en/3.1/topics/auth/default/#module-django.contrib.auth.views

https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html

https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

https://simpleisbetterthancomplex.com/tips/2016/08/04/django-tip-9-password-change-form.html

https://github.com/egorsmkv/simple-django-login-and-register

https://github.com/Antonio-Neves/Custom-User-Django-pt

https://github.com/django/django/tree/main/django/contrib/admin/templates/registration

https://github.com/django/django/blob/main/django/contrib/auth/views.py

https://github.com/django/django/blob/main/django/contrib/auth/forms.py

https://github.com/django/django/blob/main/django/contrib/auth/tokens.py
