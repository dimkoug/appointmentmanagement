from django import forms

from cms.forms import DynamicForm

from .models import Client, Appointment


class ClientForm(DynamicForm, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'last', 'address', 'telephone')

    def clean_date(self):
        data = self.cleaned_data['date']
        exists = Appointment.objects.filter(date=data)
        if exists:
            raise forms.ValidationError("Appointment exists")
        return data


class AppointmentForm(DynamicForm, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('client', 'date', 'description')

    def clean_date(self):
        data = self.cleaned_data['date']
        exists = Appointment.objects.filter(date=data)
        if exists:
            raise forms.ValidationError("Appointment exists")
        return data
