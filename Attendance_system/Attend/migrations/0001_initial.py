# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-19 10:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '0002_auto_20160116_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lock_time', models.DateTimeField()),
                ('commet', models.CharField(max_length=64)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.User')),
            ],
        ),
    ]
