# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-21 13:46
from __future__ import unicode_literals

import authentication.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phonenumber', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=20)),
                ('adress', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Account2',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phonenumber', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=20)),
                ('adress', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=20, null=True)),
                ('slug', models.SlugField(default=uuid.uuid1, unique=True)),
                ('file1', models.ImageField(blank=True, null=True, upload_to=authentication.models.upload_location)),
                ('file2', models.ImageField(blank=True, null=True, upload_to=authentication.models.upload_location)),
            ],
        ),
    ]
