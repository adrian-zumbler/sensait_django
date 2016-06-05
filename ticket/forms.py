from django import forms
from helpdesk.models import Ticket


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = '__all__'

