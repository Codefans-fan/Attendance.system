# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='mailconfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('umail', models.EmailField(max_length=254)),
                ('mail_template', models.TextField()),
                ('userid', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
