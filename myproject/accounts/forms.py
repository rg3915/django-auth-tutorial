from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
