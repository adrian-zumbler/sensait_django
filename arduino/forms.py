from django import forms

from .models import SensorType, SensorEquipment, AlertObservation


class SensorTypeForm(forms.ModelForm):
    class Meta:
        model = SensorType
        fields = '__all__'


class SensorEquipmentForm(forms.ModelForm):
    class Meta:
        model = SensorEquipment
        fields = '__all__'


class AlertObservationForm(forms.ModelForm):
    class Meta:
        model = AlertObservation
        fields = '__all__'
