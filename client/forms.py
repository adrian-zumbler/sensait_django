# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm, User


from .models import Enterprise, Client
from arduino.models import Arduino


class EnterpriseForm(forms.ModelForm):
    class Meta:
        model = Enterprise
        fields = '__all__'


class ClientCreationForm(UserCreationForm):

    error_messages = {
        'password_mismatch': "Las dos contraseñas no coinciden.",
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
        if not self.initial:
            client = Client.objects.create(
                user=user,
                enterprise=self.cleaned_data['enterprise'])
        else:
            client = Client.objects.get(user=user)
            client.enterprise = self.cleaned_data['enterprise']
            client.save()
        return client


class ArduinoSensorCSVReportForm(forms.Form):
    min_time = forms.CharField(max_length=10)
    max_time = forms.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('sensor_queryset')
        super(ArduinoSensorCSVReportForm, self).__init__(*args, **kwargs)
        self.fields['sensor'] = forms.ModelChoiceField(queryset=queryset)



