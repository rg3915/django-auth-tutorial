from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
    cpf = forms.CharField(label='CPF')
    rg = forms.CharField(label='RG', required=False)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'cpf',
            'rg',
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
    cpf = forms.CharField(label='CPF')
    rg = forms.CharField(label='RG', required=False)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'cpf',
            'rg',
            'username',
            'email',
        )
