from django import forms

from .models import SensorType, SensorEquipment


class SensorTypeForm(forms.ModelForm):
    class Meta:
        model = SensorType
        fields = '__all__'


class SensorEquipmentForm(forms.ModelForm):
    class Meta:
        model = SensorEquipment
        fields = '__all__'
