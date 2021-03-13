from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q

from core.views import CoreListView, CoreDetailView, CoreCreateView, CoreUpdateView, CoreDeleteView


from .forms import ClientForm, AppointmentForm
from .models import Client, Appointment
from .mixins import ProtectedViewMixin, SaveProfileMixin, ProtectedObjectMixin


class ClientList(ProtectedViewMixin, CoreListView):
    model = Client
    paginate_by = 100
    template='list'

    def get_queryset(self):
        qs = super().get_queryset().filter(
            profile=self.request.user.profile)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(Q(name__icontains=q) | Q(last__icontains=q))
        return qs


class ClientDetail(ProtectedViewMixin, CoreDetailView):
    model = Client
    template='detail'


class ClientCreate(ProtectedViewMixin, SaveProfileMixin, CoreCreateView):
    model = Client
    form_class = ClientForm
    template='form'


class ClientUpdate(ProtectedObjectMixin, ProtectedViewMixin, CoreUpdateView):
    model = Client
    form_class = ClientForm
    template='form'


class ClientDelete(ProtectedObjectMixin, ProtectedViewMixin, CoreDeleteView):
    model = Client
    template='confirm_delete'


class AppointmentList(ProtectedViewMixin, CoreListView):
    model = Appointment
    paginate_by = 100
    template='list'

    def get_queryset(self):
        qs = super().get_queryset().select_related('client').filter(
            client__profile=self.request.user.profile)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(
                Q(client__name__icontains=q) | Q(client__last__icontains=q))
        return qs


class AppointmentDetail(ProtectedViewMixin, CoreDetailView):
    model = Appointment
    template='detail'


class AppointmentCreate(ProtectedViewMixin, SaveProfileMixin, CoreCreateView):
    model = Appointment
    form_class = AppointmentForm
    template='form'

    def get_initial(self):
        initial = super().get_initial()
        if 'client' in self.request.GET:
            initial.update({
                'client': self.request.GET.get('client')
            })
        return initial


class AppointmentUpdate(ProtectedObjectMixin, ProtectedViewMixin, CoreUpdateView):
    model = Appointment
    form_class = AppointmentForm
    template='form'


class AppointmentDelete(ProtectedObjectMixin, ProtectedViewMixin, CoreDeleteView):
    model = Appointment
    template='confirm_delete'
