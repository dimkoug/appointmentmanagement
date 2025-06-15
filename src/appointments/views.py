from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.functions import is_ajax
from core.mixins import PaginationMixin, ModelMixin, SuccessUrlMixin,FormMixin,QueryListMixin, AjaxDeleteMixin


from .forms import ClientForm, AppointmentForm
from .models import Client, Appointment
from .mixins import ProtectedViewMixin, SaveProfileMixin, ProtectedObjectMixin

class BaseListView(PaginationMixin,QueryListMixin,ModelMixin, LoginRequiredMixin, ListView):
    def dispatch(self, *args, **kwargs):
        self.ajax_list_partial = '{}/partials/{}_list_partial.html'.format(self.model._meta.app_label,self.model.__name__.lower())
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if is_ajax(request):
            html_form = render_to_string(
                self.ajax_list_partial, context, request)
            return JsonResponse(html_form, safe=False)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            queryset = queryset.filter(profile_id=self.request.user.profile.id)
        except:
            queryset = queryset.filter(client__profile_id=self.request.user.profile.id)
        return queryset


class ClientList(BaseListView):
    model = Client
    paginate_by = 100

    # def get_queryset(self):
    #     qs = super().get_queryset().filter(
    #         profile=self.request.user.profile)
    #     q = self.request.GET.get('q')
    #     if q and q != '':
    #         qs = qs.filter(Q(name__icontains=q) | Q(last__icontains=q))
    #     return qs


class ClientDetail(LoginRequiredMixin, DetailView):
    model = Client
    queryset = Client.objects.select_related(
                    'profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset



class ClientCreate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, CreateView):
    model = Client
    form_class = ClientForm

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)



class ClientUpdate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, UpdateView):
    model = Client
    form_class = ClientForm
    queryset = Client.objects.select_related(
                    'profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class ClientDelete(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,AjaxDeleteMixin,DeleteView):
    model = Client
    ajax_partial = 'partials/ajax_delete_modal.html'

    queryset = Client.objects.select_related(
                    'profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class AppointmentList(BaseListView):
    model = Appointment
    paginate_by = 100


    # def get_queryset(self):
    #     qs = super().get_queryset().select_related('client').filter(
    #         client__profile=self.request.user.profile)
    #     q = self.request.GET.get('q')
    #     if q and q != '':
    #         qs = qs.filter(
    #             Q(client__name__icontains=q) | Q(client__last__icontains=q))
    #     return qs


class AppointmentDetail(LoginRequiredMixin, DetailView):
    model = Appointment
    queryset = Appointment.objects.select_related(
                    'client__profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client__profile_id=self.request.user.profile.id)
        return queryset


class AppointmentCreate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template='form'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        if 'client' in self.request.GET:
            initial.update({
                'client': self.request.GET.get('client')
            })
        return initial


class AppointmentUpdate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    queryset = Appointment.objects.select_related(
                    'client__profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client__profile_id=self.request.user.profile.id)
        return queryset


class AppointmentDelete(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,AjaxDeleteMixin,DeleteView):
    model = Appointment
    ajax_partial = 'partials/ajax_delete_modal.html'

    queryset = Appointment.objects.select_related(
                    'client__profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client__profile_id=self.request.user.profile.id)
        return queryset
