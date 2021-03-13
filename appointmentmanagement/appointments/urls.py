from django.urls import path

from .views import (
    ClientList, ClientDetail, ClientCreate, ClientUpdate,
    ClientDelete, AppointmentList, AppointmentDetail, AppointmentCreate,
    AppointmentUpdate, AppointmentDelete
)

app_name='appointments'
urlpatterns = [
    path('', AppointmentList.as_view(), name='appointment-list'),
    path('<int:pk>/', AppointmentDetail.as_view(),
         name='appointment-detail'),
    path('create/', AppointmentCreate.as_view(),
         name='appointment-create'),
    path('<int:pk>/update/', AppointmentUpdate.as_view(),
         name='appointment-update'),
    path('<int:pk>/delete', AppointmentDelete.as_view(),
         name='appointment-delete'),

    path('clients/', ClientList.as_view(), name='client-list'),
    path('client/<int:pk>/', ClientDetail.as_view(),
         name='client-detail'),
    path('client/create/', ClientCreate.as_view(),
         name='client-create'),
    path('client/<int:pk>/update/', ClientUpdate.as_view(),
         name='client-update'),
    path('client/<int:pk>/delete', ClientDelete.as_view(),
         name='client-delete'),

]
