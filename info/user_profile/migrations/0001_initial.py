# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-02 12:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mesaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mesaj', models.CharField(max_length=1000)),
                ('slug', models.SlugField(default=uuid.uuid1, unique=True)),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mesaje', to=settings.AUTH_USER_MODEL)),
                ('destinatar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mesajee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
