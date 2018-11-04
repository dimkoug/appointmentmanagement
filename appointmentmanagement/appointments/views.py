from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q

from cms.views import BaseList, BaseDetail, BaseCreate, BaseUpdate, BaseDelete


from .forms import ClientForm, AppointmentForm
from .models import Client, Appointment
from .mixins import ProtectedViewMixin, SaveProfileMixin


class ClientList(ProtectedViewMixin, BaseList):
    model = Client
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset().filter(
            profile=self.request.user.profile_user)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(Q(name__icontains=q) | Q(last__icontains=q))
        return qs


class ClientDetail(ProtectedViewMixin, BaseDetail):
    model = Client


class ClientCreate(ProtectedViewMixin, SaveProfileMixin, BaseCreate):
    model = Client
    form_class = ClientForm


class ClientUpdate(ProtectedViewMixin, BaseUpdate):
    model = Client
    form_class = ClientForm


class ClientDelete(ProtectedViewMixin, BaseDelete):
    model = Client
    success_url = reverse_lazy('client-list')


class AppointmentList(ProtectedViewMixin, BaseList):
    model = Appointment
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset().filter(
            profile=self.request.user.profile_user)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(
                Q(client__name__icontains=q) | Q(client__last__icontains=q))
        return qs


class AppointmentDetail(ProtectedViewMixin, BaseDetail):
    model = Appointment


class AppointmentCreate(ProtectedViewMixin, SaveProfileMixin, BaseCreate):
    model = Appointment
    form_class = AppointmentForm

    def get_initial(self):
        initial = super().get_initial()
        if 'client' in self.request.GET:
            initial.update({
                'client': self.request.GET.get('client')
            })
        return initial


class AppointmentUpdate(ProtectedViewMixin, BaseUpdate):
    model = Appointment
    form_class = AppointmentForm


class AppointmentDelete(ProtectedViewMixin, BaseDelete):
    model = Appointment
    success_url = reverse_lazy('appointment-list')
