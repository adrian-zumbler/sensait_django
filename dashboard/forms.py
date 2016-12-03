from django import forms

from arduino.models import Arduino, SensorType, ArduinoSensor
from client.models import Project, Client
from django.forms.utils import ErrorList

class AdminProjectCreateForm(forms.ModelForm):
    name = forms.RegexField(r'[A-Za-z]+')

    class Meta:
        model = Project
        exclude = ('clients', )


class AdminProjectUpdateForm(forms.ModelForm):
    name = forms.RegexField(r'[A-Za-z]+')

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):

        super(AdminProjectUpdateForm, self).__init__(
            data, files, auto_id, prefix, initial, error_class,
            label_suffix, empty_permitted, instance)

        queryset = Client.objects.filter(enterprise=instance.enterprise)

        self.fields['clients'] = forms.ModelMultipleChoiceField(
            queryset=queryset
        )

        clients = self.fields

    class Meta:
        model = Project
        fields = '__all__'


class AdminArduinoCreateForm(forms.ModelForm):
    name = forms.RegexField(r'[A-Za-z]+')

    class Meta:
        model = Arduino
        fields = ['name', 'location', 'correos_alertas', 'delta_time_alerts']


class AdminSensorCreateForm(forms.ModelForm):

    class Meta:
        model = Arduino
        fields = '__all__'


class AdminInlineArduinoSensorCreateForm(forms.ModelForm):

    class Meta:
        model = SensorType
        fields = '__all__'


ArduinoSensorFormSet = forms.modelformset_factory(
    ArduinoSensor,
    exclude=('arduino',),
    extra=2
)

InLineArduinoSensorFormSet = forms.inlineformset_factory(
    Arduino,
    ArduinoSensor,
    fields='__all__',
    extra=2
)
