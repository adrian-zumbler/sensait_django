from django import forms
from helpdesk.models import Ticket, FollowUp


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = '__all__'


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        exclude = ('ticket', )

