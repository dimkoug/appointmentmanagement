from django import forms

from core.forms import BootstrapForm

from .models import Client, Appointment


class ClientForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'last', 'address', 'telephone')


class AppointmentForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('client', 'date', 'description')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.select_related('profile').filter(profile_id=self.request.user.profile)

