# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FailedAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255, verbose_name=b'Username')),
                ('IP', models.IPAddressField(null=True, verbose_name=b'IP Address')),
                ('failures', models.PositiveIntegerField(default=0, verbose_name=b'Failures')),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name=b'Last failed attempt')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='failedattempt',
            unique_together=set([('username', 'IP')]),
        ),
    ]
