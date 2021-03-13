# Generated by Django 3.1.7 on 2021-03-13 07:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('last', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('telephone', models.CharField(blank=True, max_length=100)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='profiles.profile')),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
                'ordering': ('-created_at',),
                'default_related_name': 'clients',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='appointments.client')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='profiles.profile')),
            ],
            options={
                'verbose_name': 'appointment',
                'verbose_name_plural': 'appointments',
                'ordering': ('-created_at',),
                'default_related_name': 'appointments',
            },
        ),
    ]
