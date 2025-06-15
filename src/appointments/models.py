import datetime
from django.db import models

from profiles.models import Profile
from core.models import Timestamped


class Client(Timestamped):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
    address = models.CharField(blank=True, max_length=100)
    telephone = models.CharField(blank=True, max_length=100)

    class Meta:
        default_related_name = 'clients'
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        ordering = ('-created',)

    def __str__(self):
        return self.name


class Appointment(Timestamped):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        default_related_name = 'appointments'
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'
        ordering = ('-created',)

    def __str__(self):
        return "Appointment for {} {}".format(
            self.client.name, self.client.last)
