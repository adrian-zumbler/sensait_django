from django import forms

from .models import SensorType


class SensorTypeForm(forms.ModelForm):
    class Meta:
        model = SensorType
        fields = '__all__'

