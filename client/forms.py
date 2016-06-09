# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, User


from .models import Enterprise, Client


class EnterpriseForm(forms.ModelForm):
    class Meta:
        model = Enterprise
        fields = '__all__'


class ClientCreationForm(UserCreationForm):

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.")
    enterprise = forms.ModelChoiceField(
        queryset=Enterprise.objects.all(),
        empty_label='',
        label="Empresa")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        user = super(ClientCreationForm, self).save(commit=True)
        client = Client.objects.create(
            user=user,
            enterprise=self.cleaned_data['enterprise'])
        return client


