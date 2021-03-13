from django import forms

from core.forms import BootstrapForm

from .models import Client, Appointment


class ClientForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'last', 'address', 'telephone')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_date(self):
        data = self.cleaned_data['date']
        exists = Appointment.objects.filter(date=data)
        if exists:
            raise forms.ValidationError("Appointment exists")
        return data


class AppointmentForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('client', 'date', 'description')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_date(self):
        data = self.cleaned_data['date']
        exists = Appointment.objects.filter(date=data)
        if exists:
            raise forms.ValidationError("Appointment exists")
        return data
